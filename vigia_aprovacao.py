#!/usr/bin/env python3
"""Vigia da aprovação por e-mail.

Verifica, a cada N minutos, se a Verônica já respondeu o e-mail de aprovação
de algum tema que está com status `pendente`. Lê o thread no Gmail pelo MCP do
Composio, procura APROVAR / REJEITAR na resposta e atualiza o estado com
`aprovacao.py marcar`.

Quando o veredito é `APROVAR`, o vigia publica o post no Instagram na mesma
passada — mas só depois de marcar o status como aprovado. Nenhum container é
criado antes da resposta: o prazo de 24h do Instagram continua respeitado.
`REJEITAR` nunca publica. Se o publish falhar, o tema fica `aprovado` com o
erro registrado e é tentado de novo nos próximos ciclos (até 5 tentativas).

Uso:
    python3 vigia_aprovacao.py                       # verifica uma vez
    python3 vigia_aprovacao.py --slug novembro-azul
    python3 vigia_aprovacao.py --dry-run             # só mostra o que faria
    python3 vigia_aprovacao.py --sem-publicar        # só marca o status
    python3 vigia_aprovacao.py --loop                # a cada 5 minutos
    python3 vigia_aprovacao.py --loop --interval 120

O log fica em `aprovacoes/vigia.log`.
"""

import argparse
import base64
import fcntl
import json
import os
import re
import subprocess
import sys
import time
from contextlib import contextmanager
from html import unescape

import publicar_instagram
from aprovacao import BASE_DIR, agora, carregar, registrar_evento, salvar
from composio_mcp import chamar_mcp

LOG_PATH = BASE_DIR / "aprovacoes" / "vigia.log"
CAMINHO_TRAVA = BASE_DIR / "aprovacoes" / ".vigia.lock"
INTERVALO_PADRAO = 300
TENTATIVAS_REDE = 2
MAX_TENTATIVAS_PUBLICACAO = 5

# Só este endereço pode aprovar (e só ele recebe o e-mail de aprovação).
# Qualquer outra pessoa no thread — ou um e-mail reencaminhado — não publica
# nada. A regra do projeto é "nunca publicar sem aprovação explícita".
EMAIL_DONO = os.environ.get(
    "APROVACAO_EMAIL", "veronicabomfim.nutri@gmail.com"
).strip().lower()

# Emergency escape hatch (diagnóstico): aceita resposta de qualquer remetente.
# Desligado por padrão — usar só se o proxy não entregar o cabeçalho From.
ACEITAR_QUALQUER_REMETENTE = os.environ.get(
    "APROVACAO_ACEITAR_REMETENTE", ""
).strip().lower() in ("1", "true", "sim", "yes")

# "Em ... escreveu:" / "On ... wrote:" — início da citação numa resposta
RE_INICIO_CITACAO = re.compile(
    r"(?im)^\s*(em .{0,300}escreveu:.*|on .{0,300}wrote:.*|-{2,}\s*original message\s*-{2,}.*)\s*$"
)
RE_VEREDITO_LINHA = re.compile(r"^(APROVAR|REJEITAR)\b(.*)$", re.IGNORECASE)
# Palavras que transformam "APROVAR" em adiamento, dúvida ou negação.
RE_BLOQUEIO_APROVAR = re.compile(
    r"\b(depois|mais\s+tarde|futuro\w*|amanh[ãa]|quando|assim\s+que|logo|aguarde|"
    r"retom\w+|volto|aviso|fal[oô]|vejo|n[ãa]o|nao|nunca|talvez|acho\s+que|"
    r"ser[áa]|sera|preciso|falta|aguarda|retorno)\b",
    re.IGNORECASE,
)
RE_EMAIL = re.compile(r"[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}", re.IGNORECASE)
LIMITE_RESPOSTA_CURTA = 200  # sem veredito na 1ª linha, só vale resposta curta


# ------------------------------------------------------------------- log


def log(mensagem, silencioso=False):
    linha = f"{agora()}  {mensagem}"
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as arquivo:
        arquivo.write(linha + "\n")
    if not silencioso:
        print(linha, flush=True)


@contextmanager
def trava_vigia():
    """Trava de execução: só um vigia publica por vez.

    O timer do systemd e uma chamada manual podem coincidir. Sem esta trava,
    os dois processos enxergam o mesmo tema `aprovado` e publicam em
    duplicidade. Quem não consegue a trava simplesmente não roda.
    """
    CAMINHO_TRAVA.parent.mkdir(parents=True, exist_ok=True)
    arquivo = CAMINHO_TRAVA.open("a+")
    try:
        try:
            fcntl.flock(arquivo, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            yield False
            return
        try:
            yield True
        finally:
            fcntl.flock(arquivo, fcntl.LOCK_UN)
    finally:
        arquivo.close()


def notificar(titulo, mensagem):
    """Aviso de desktop; se não der, o log já registrou."""
    try:
        subprocess.run(
            ["notify-send", "-a", "Vigia de aprovação", titulo, mensagem],
            check=False,
            timeout=10,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.SubprocessError):
        pass


# -------------------------------------------------------- acesso ao Gmail


def gmail_api(endpoint, parametros=None, timeout=120):
    """GET na API do Gmail pelo proxy do Composio.

    Usamos a API direto (e não `GMAIL_FETCH_MESSAGE_BY_THREAD_ID`) porque ela
    devolve o thread inteiro num payload enorme e às vezes volta vazia quando
    existe rascunho no thread. Aqui listamos as mensagens em `minimal` e só
    baixamos o corpo das que interessam.
    """
    dados = chamar_mcp(
        "COMPOSIO_PROXY_EXECUTE",
        {
            "toolkit_slug": "gmail",
            "endpoint": endpoint,
            "method": "GET",
            "parameters": [
                {"name": nome, "value": valor, "type": "query"}
                for nome, valor in (parametros or [])
            ],
        },
        timeout=timeout,
    )
    status = dados.get("status")
    if status and int(status) != 200:
        raise RuntimeError(f"Gmail API {endpoint}: HTTP {status}")
    recurso = dados.get("data")
    if not isinstance(recurso, dict) or not recurso:
        raise RuntimeError(f"Gmail API {endpoint}: resposta vazia")
    return recurso


def listar_mensagens(thread_id):
    """Mensagens do thread, em ordem, sem rascunhos."""
    thread = gmail_api(
        f"/gmail/v1/users/me/threads/{thread_id}", [("format", "minimal")]
    )
    mensagens = thread.get("messages")
    if not isinstance(mensagens, list) or not mensagens:
        raise RuntimeError(f"thread {thread_id} sem mensagens legíveis")

    limpas = []
    for mensagem in mensagens:
        rotulos = mensagem.get("labelIds") or []
        if "DRAFT" in rotulos:
            continue  # rascunho não é resposta
        limpas.append(
            {
                "messageId": mensagem.get("id"),
                "labelIds": rotulos,
                "internalDate": int(mensagem.get("internalDate") or 0),
                "snippet": mensagem.get("snippet") or "",
            }
        )
    limpas.sort(key=lambda m: m["internalDate"])
    return limpas


def _partes(payload, acumulado):
    acumulado.append(payload)
    for parte in payload.get("parts") or []:
        _partes(parte, acumulado)


def _decodificar(parte):
    dados = (parte.get("body") or {}).get("data")
    if not dados:
        return ""
    return base64.urlsafe_b64decode(dados + "=" * (-len(dados) % 4)).decode(
        "utf-8", "replace"
    )


def texto_da_mensagem(payload):
    """Texto do corpo: prefere text/plain, cai para text/html."""
    partes = []
    _partes(payload or {}, partes)
    for mime in ("text/plain", "text/html"):
        for parte in partes:
            if parte.get("mimeType") != mime or parte.get("filename"):
                continue
            texto = _decodificar(parte)
            if texto.strip():
                return texto
    return ""


def _cabecalho(cabecalhos, nome):
    """Valor de um cabeçalho do e-mail (From, Subject, ...)."""
    return next(
        (
            h.get("value")
            for h in cabecalhos
            if (h.get("name") or "").lower() == nome.lower()
        ),
        "",
    )


def buscar_conteudo(message_id):
    """Corpo da mensagem.

    `format=full` às vezes volta vazio pelo proxy (mensagens grandes, tipo
    resposta que cita o e-mail inteiro). Nesse caso caímos para `metadata`,
    cujo `snippet` traz o começo da resposta — exatamente onde fica o veredito.
    """
    assunto = ""
    remetente = ""
    try:
        mensagem = gmail_api(
            f"/gmail/v1/users/me/messages/{message_id}", [("format", "full")]
        )
        cabecalhos = (mensagem.get("payload") or {}).get("headers") or []
        assunto = _cabecalho(cabecalhos, "subject")
        remetente = _cabecalho(cabecalhos, "from")
        texto = texto_da_mensagem(mensagem.get("payload") or {})
        if texto.strip():
            return {
                "messageId": mensagem.get("id") or message_id,
                "messageText": texto,
                "snippet": "",
                "subject": assunto,
                "remetente": remetente,
            }
    except RuntimeError:
        pass

    meta = gmail_api(
        f"/gmail/v1/users/me/messages/{message_id}", [("format", "metadata")]
    )
    cabecalhos = (meta.get("payload") or {}).get("headers") or []
    assunto = assunto or _cabecalho(cabecalhos, "subject")
    remetente = remetente or _cabecalho(cabecalhos, "from")
    return {
        "messageId": meta.get("id") or message_id,
        "messageText": "",
        "snippet": meta.get("snippet") or "",
        "subject": assunto,
        "remetente": remetente,
    }


# ------------------------------------------------------- leitura da resposta


def texto_limpo(mensagem):
    """Texto da mensagem sem HTML e sem o e-mail original citado.

    Essencial: o e-mail de aprovação contém as palavras APROVAR e REJEITAR nas
    instruções, e o Gmail cita a mensagem original na resposta. Sem cortar a
    citação, toda resposta pareceria um veredito.
    """
    bruto = mensagem.get("messageText") or ""
    if not bruto.strip():
        bruto = mensagem.get("snippet") or ""

    corte = len(bruto)
    for marcador in ("gmail_quote", "<blockquote", "moz-cite-prefix", "yahoo_quoted"):
        posicao = bruto.find(marcador)
        if posicao != -1:
            corte = min(corte, posicao)
    bruto = bruto[:corte]
    bruto = re.sub(r"<[^>]*$", "", bruto)  # tag cortada ao meio pela citação

    bruto = re.sub(r"(?i)<br\s*/?>", "\n", bruto)
    bruto = re.sub(r"(?i)</(p|div|tr|li|h[1-6]|blockquote)>", "\n", bruto)
    bruto = re.sub(r"<[^>]+>", " ", bruto)
    bruto = unescape(bruto)

    linhas = [l for l in bruto.splitlines() if not l.lstrip().startswith(">")]
    texto = "\n".join(linhas)

    inicio = RE_INICIO_CITACAO.search(texto)
    if inicio:
        texto = texto[: inicio.start()]
    return texto.strip()


def remetente_de(mensagem):
    """Endereço de quem enviou a mensagem (cabeçalho From)."""
    bruto = mensagem.get("remetente") or ""
    achado = RE_EMAIL.search(bruto)
    return achado.group(0).lower() if achado else ""


def remetente_permitido(mensagem):
    """Só a conta da proprietária pode aprovar.

    Sem remetente legível a resposta é descartada (falha para o lado seguro):
    melhor ficar pendente do que publicar sem aprovação explícita.
    """
    return remetente_de(mensagem) == EMAIL_DONO


def _veredito_na_linha(linha):
    """(veredito, resto) se a linha abre com APROVAR/REJEITAR; senão None."""
    texto = linha.strip().strip("\"“”'‘’()[]{}").strip()
    achado = RE_VEREDITO_LINHA.match(texto)
    if not achado:
        return None
    return achado.group(1).upper(), achado.group(2).strip()


def _aprovacao_e_confiavel(resto):
    """APROVAR só vale quando não há dúvida, negação ou adiamento.

    "APROVAR", "APROVAR, pode publicar!" e "Aprovar, obrigada" aprovam.
    "APROVAR depois", "APROVAR?" e "não APROVAR" não aprovam — nesses casos
    o post continua pendente.
    """
    if "?" in resto or "？" in resto:
        return False
    return not RE_BLOQUEIO_APROVAR.search(resto)


def _resultado_do_veredito(veredito, resto, texto_completo):
    if veredito == "APROVAR":
        return "aprovado", ""
    motivo = ""
    achado = re.search(r"REJEITAR", texto_completo, re.IGNORECASE)
    if achado:
        motivo = re.sub(r"\s+", " ", texto_completo[achado.end() :]).strip(
            " .:-,;–—"
        )[:300]
    return "rejeitado", motivo


def classificar(mensagem):
    """Devolve (status, motivo) ou None se a mensagem não traz veredito.

    Aceita o veredito no começo da primeira linha ("APROVAR", "REJEITAR + o
    que corrigir") ou, no máximo, numa resposta curta — para não confundir
    conversa ("só vou aprovar depois de ver") com aprovação.
    """
    texto = texto_limpo(mensagem)
    if not texto:
        return None

    linhas = [l.strip() for l in texto.splitlines() if l.strip()]
    if not linhas:
        return None

    junto = " ".join(linhas)

    achado = _veredito_na_linha(linhas[0])
    if achado:
        veredito, resto = achado
        if veredito == "APROVAR" and not _aprovacao_e_confiavel(resto):
            return None
        return _resultado_do_veredito(veredito, resto, junto)

    # Sem veredito na primeira linha, só vale resposta curta e com o
    # veredito abrindo alguma linha ("Oi!\nAPROVAR").
    if len(junto) > LIMITE_RESPOSTA_CURTA:
        return None
    for linha in linhas[:5]:
        achado = _veredito_na_linha(linha)
        if not achado:
            continue
        veredito, resto = achado
        if veredito == "APROVAR" and not _aprovacao_e_confiavel(resto):
            continue
        return _resultado_do_veredito(veredito, resto, junto)
    return None


def indice_da_aprovacao(mensagens, dados):
    """Índice da mensagem do e-mail de aprovação; None se não achar.

    O e-mail de aprovação é a mensagem que **abriu** o thread. No Gmail, o id
    do thread é o id da primeira mensagem — por isso o `thread_id` é a âncora
    mais confiável. Sem ele, usamos a primeira mensagem, desde que seja nossa
    (label SENT).

    Atenção: `email.message_id` guarda o id da mensagem que carregou o
    veredito (é o que o vigia grava ao marcar), e não serve como âncora.

    Devolver None é sinal de "não identifico o e-mail": o chamador precisa
    falhar para o lado seguro (não varrer o thread inteiro).
    """
    if not mensagens:
        return None

    email = dados.get("email") or {}
    thread_id = email.get("thread_id")
    if thread_id:
        for indice, mensagem in enumerate(mensagens):
            if mensagem["messageId"] == thread_id and "SENT" in mensagem["labelIds"]:
                return indice

    if "SENT" in mensagens[0]["labelIds"]:
        return 0
    return None


# -------------------------------------------------------------- verificação


def _salvar_vigia(dados, dry_run=False, contar=True, **campos):
    if dry_run:
        return
    vigia = dados.setdefault("vigia", {})
    vigia["ultima_verificacao"] = agora()
    if contar:
        vigia["verificacoes"] = vigia.get("verificacoes", 0) + 1
    vigia.update(campos)
    salvar(dados)


def _marcar(slug, status, message_id, motivo=""):
    comando = [
        sys.executable,
        str(BASE_DIR / "aprovacao.py"),
        "marcar",
        slug,
        status,
        "--message-id",
        message_id,
    ]
    if motivo:
        # `--detalhe=<valor>`: o motivo vem do e-mail e não pode ser lido
        # como opção pelo argparse (argument injection).
        comando.append(f"--detalhe={motivo}")
    resultado = subprocess.run(
        comando, cwd=BASE_DIR, capture_output=True, text=True, timeout=60
    )
    saida = (resultado.stdout or "").strip()
    if resultado.returncode != 0:
        erro = (resultado.stderr or saida or "erro desconhecido").strip()
        raise RuntimeError(f"aprovacao.py marcar falhou: {erro}")
    return saida


def _atualizar_publicacao(dados, campos):
    """Persiste o progresso do publish para sobreviver a uma queda no meio."""
    publicacao = dados.setdefault("publicacao", {})
    publicacao.update(campos)
    publicacao["atualizado_em"] = agora()
    salvar(dados)


def _registrar_topico(dados):
    """Marca o tema em posted_topics.json, como no fluxo manual."""
    titulo = (dados.get("titulo") or dados.get("slug") or "").strip()
    if not titulo:
        return
    try:
        subprocess.run(
            [sys.executable, str(BASE_DIR / "topic_manager.py"), "add", titulo],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.SubprocessError):
        pass


def _publicar_aprovado(slug, dados, silencioso=False, dry_run=False):
    """Publica um tema com status `aprovado` (com retentativas limitadas)."""
    publicacao = dados.setdefault("publicacao", {})
    if publicacao.get("desistiu"):
        log(
            f"{slug}  ⚠️  publicação automática desistiu — publique manualmente",
            silencioso,
        )
        return True

    tentativas = int(publicacao.get("tentativas") or 0)
    if tentativas >= MAX_TENTATIVAS_PUBLICACAO:
        publicacao["desistiu"] = True
        publicacao["erro"] = publicacao.get("erro") or "limite de tentativas"
        publicacao["atualizado_em"] = agora()
        registrar_evento(
            dados, "publicacao", f"desistiu após {tentativas} tentativa(s)"
        )
        salvar(dados)
        log(
            f"{slug}  ❌ publicação falhou {tentativas}x — desistindo; "
            "publique manualmente",
            silencioso,
        )
        notificar(
            "Publicação falhou",
            f"{slug}: {tentativas} tentativas. Publique manualmente.",
        )
        return False

    if dry_run:
        log(
            f"{slug}  [dry-run] publicaria {len(dados.get('imagens') or [])} "
            "imagem(ns) no Instagram",
            silencioso,
        )
        return True

    tentativas += 1
    publicacao["tentativas"] = tentativas
    publicacao["erro"] = None
    publicacao["atualizado_em"] = agora()
    salvar(dados)
    log(
        f"{slug}  📤 publicando no Instagram "
        f"(tentativa {tentativas}/{MAX_TENTATIVAS_PUBLICACAO})",
        silencioso,
    )

    try:
        resultado = publicar_instagram.publicar(
            dados, ao_progredir=lambda progresso: _atualizar_publicacao(dados, progresso)
        )
    except Exception as erro:  # noqa: BLE001
        publicacao = dados.setdefault("publicacao", {})
        publicacao["tentativas"] = tentativas
        publicacao["erro"] = str(erro)[:500]
        publicacao.setdefault("fase", "falha")
        publicacao["atualizado_em"] = agora()
        registrar_evento(
            dados, "publicacao", f"tentativa {tentativas} falhou: {str(erro)[:200]}"
        )
        salvar(dados)
        log(f"{slug}  ❌ publicação falhou: {erro}", silencioso)
        if tentativas == 1:
            notificar("Falha ao publicar", f"{slug}: {str(erro)[:150]}")
        return False

    dados["status"] = "publicado"
    dados["publicacao"] = {
        **resultado,
        "tentativas": tentativas,
        "publicado_em": resultado.get("publicado_em") or agora(),
    }
    registrar_evento(
        dados,
        "publicado",
        resultado.get("permalink") or resultado.get("media_id") or "",
    )
    salvar(dados)
    _registrar_topico(dados)

    link = resultado.get("permalink") or resultado.get("media_id") or ""
    log(f"{slug}  ✅ publicado no Instagram: {link}", silencioso)
    notificar("Publicado no Instagram", f"{slug}: {link}")
    return True


def verificar(slug, silencioso=False, dry_run=False, publicar=True):
    """Verifica um tema. Devolve True se a checagem rodou sem erro."""
    dados = carregar(slug)
    if not dados:
        log(f"{slug}  ⚠️  estado não encontrado", silencioso)
        return False

    status = dados.get("status")
    if status == "publicado":
        log(f"{slug}  publicado — nada a fazer", silencioso)
        return True
    if status == "aprovado":
        if not publicar:
            log(f"{slug}  aprovado — publicação automática desligada", silencioso)
            return True
        return _publicar_aprovado(slug, dados, silencioso, dry_run)
    if status != "pendente":
        log(f"{slug}  {status} — nada a verificar", silencioso)
        return True

    thread_id = (dados.get("email") or {}).get("thread_id")
    if not thread_id:
        _salvar_vigia(dados, dry_run=dry_run, erro="e-mail sem thread_id")
        log(f"{slug}  ⚠️  sem thread_id no estado", silencioso)
        return False

    ultimo_erro = None
    for tentativa in range(1, TENTATIVAS_REDE + 1):
        try:
            mensagens = listar_mensagens(thread_id)
            break
        except Exception as erro:  # rede, MCP, Composio, Gmail
            ultimo_erro = erro
            if tentativa < TENTATIVAS_REDE:
                time.sleep(3)
    else:
        _salvar_vigia(dados, dry_run=dry_run, erro=str(ultimo_erro)[:300])
        log(f"{slug}  ❌ {ultimo_erro}", silencioso)
        return False

    indice = indice_da_aprovacao(mensagens, dados)
    if indice is None:
        # Fail-safe: sem e-mail de aprovação identificado, nenhuma mensagem do
        # thread vale como resposta. Varrer tudo permitiria que uma mensagem
        # solta (ou o próprio e-mail de aprovação) virar aprovação.
        _salvar_vigia(dados, dry_run=dry_run, erro="e-mail de aprovação não identificado")
        log(
            f"{slug}  ⚠️  e-mail de aprovação não identificado no thread — "
            "nenhuma resposta é considereda (fail-safe)",
            silencioso,
        )
        return False

    # Só conta como resposta o que veio depois do e-mail de aprovação (e não
    # antes dele no tempo).
    limite = mensagens[indice].get("internalDate") or 0
    candidatas = [
        m for m in mensagens[indice + 1 :] if (m.get("internalDate") or 0) >= limite
    ]

    vigia = dados.get("vigia") or {}
    ja_lida = vigia.get("resposta_id")
    veredito = None
    for mensagem in candidatas:
        if mensagem["messageId"] == ja_lida:
            continue
        try:
            conteudo = buscar_conteudo(mensagem["messageId"])
        except Exception as erro:
            _salvar_vigia(dados, dry_run=dry_run, erro=str(erro)[:300])
            log(f"{slug}  ❌ {erro}", silencioso)
            return False
        if not ACEITAR_QUALQUER_REMETENTE and not remetente_permitido(conteudo):
            quem = remetente_de(conteudo) or "desconhecido"
            log(
                f"{slug}  ⚠️  resposta ignorada — remetente não autorizado ({quem})",
                silencioso,
            )
            continue
        resultado = classificar(conteudo)
        if resultado:
            veredito = (conteudo, resultado)

    ultima = (
        candidatas[-1]["messageId"]
        if candidatas
        else (mensagens[-1]["messageId"] if mensagens else vigia.get("ultimo_message_id"))
    )
    _salvar_vigia(dados, dry_run=dry_run, ultimo_message_id=ultima, erro=None)

    if not veredito:
        resumo = (
            f"{len(candidatas)} resposta(s) sem veredito"
            if candidatas
            else "sem resposta nova"
        )
        log(f"{slug}  pendente — {resumo}", silencioso)
        return True

    conteudo, (status, motivo) = veredito
    message_id = conteudo["messageId"]

    if dry_run:
        log(
            f"{slug}  [dry-run] veredito {status.upper()} em {message_id}"
            + (f" — {motivo}" if motivo else ""),
            silencioso,
        )
        return True

    try:
        saida = _marcar(slug, status, message_id, motivo)
    except Exception as erro:
        _salvar_vigia(dados, erro=str(erro)[:300])
        log(f"{slug}  ❌ {erro}", silencioso)
        return False

    dados = carregar(slug) or dados
    _salvar_vigia(
        dados,
        contar=False,
        resposta_id=message_id,
        resultado=status,
        motivo=motivo,
        erro=None,
    )
    registrar_evento(
        dados,
        "vigia",
        f"resposta {message_id} → {status}" + (f" ({motivo})" if motivo else ""),
    )
    salvar(dados)

    log(f"{slug}  {saida or status.upper()}" + (f" — {motivo}" if motivo else ""))
    if status == "aprovado":
        notificar("Carrossel aprovado", f"{slug}: APROVAR recebido.")
        if publicar:
            return _publicar_aprovado(slug, dados, silencioso, dry_run)
    else:
        notificar(
            "Carrossel rejeitado",
            f"{slug}: REJEITAR" + (f" — {motivo[:120]}" if motivo else ""),
        )
    return True


def alvos(publicar=True):
    """Temas que merecem uma passada do vigia.

    Pendentes sempre; aprovados só quando a publicação automática está ligada
    e ainda não desistiu.
    """
    slugs = []
    for arquivo in sorted((BASE_DIR / "aprovacoes").glob("*.json")):
        try:
            dados = json.loads(arquivo.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        slug = dados.get("slug")
        if not slug:
            continue
        status = dados.get("status")
        if status == "pendente":
            slugs.append(slug)
        elif (
            publicar
            and status == "aprovado"
            and not (dados.get("publicacao") or {}).get("desistiu")
        ):
            slugs.append(slug)
    return slugs


def verificar_todas(temas=None, silencioso=False, dry_run=False, publicar=True):
    lista = temas or alvos(publicar)
    if not lista:
        log("nenhuma aprovação pendente", silencioso)
        return True
    resultados = [verificar(slug, silencioso, dry_run, publicar) for slug in lista]
    return all(resultados)


# --------------------------------------------------------------------- CLI


def laco(intervalo, slugs, silencioso=False, dry_run=False, publicar=True):
    log(f"vigia iniciado — intervalo de {intervalo}s", silencioso)
    falhas = 0
    while True:
        try:
            ok = verificar_todas(slugs, silencioso, dry_run, publicar)
            falhas = 0 if ok else falhas + 1
        except KeyboardInterrupt:
            log("vigia interrompido", silencioso)
            return
        except Exception as erro:
            falhas += 1
            log(f"erro inesperado: {erro}", silencioso)

        espera = intervalo
        if falhas >= 3:
            espera = min(intervalo * (2 ** (falhas - 2)), 1800)
            log(f"{falhas} falhas seguidas — próxima em {espera}s", silencioso)
        try:
            time.sleep(espera)
        except KeyboardInterrupt:
            log("vigia interrompido", silencioso)
            return


def main():
    parser = argparse.ArgumentParser(description="Vigia do e-mail de aprovação")
    parser.add_argument("--once", action="store_true", help="verifica uma vez (padrão)")
    parser.add_argument("--loop", action="store_true", help="verifica continuamente")
    parser.add_argument(
        "--interval",
        type=int,
        default=INTERVALO_PADRAO,
        help=f"segundos entre verificações no modo --loop (padrão {INTERVALO_PADRAO})",
    )
    parser.add_argument("--slug", help="verifica só um tema")
    parser.add_argument("--silencioso", action="store_true", help="só grava no log")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="mostra o que faria, sem alterar o estado dos temas",
    )
    parser.add_argument(
        "--sem-publicar",
        action="store_true",
        help="só marca o status; não publica no Instagram automaticamente",
    )
    parser.add_argument(
        "--aceitar-qualquer-remetente",
        action="store_true",
        help="diagnóstico: aceita aprovação de qualquer remetente do thread",
    )
    args = parser.parse_args()

    if args.interval < 30:
        raise SystemExit("❌ --interval mínimo de 30 segundos")

    global ACEITAR_QUALQUER_REMETENTE
    if args.aceitar_qualquer_remetente:
        ACEITAR_QUALQUER_REMETENTE = True
        log("⚠️  aceitando aprovação de qualquer remetente do thread", args.silencioso)

    publicar = not args.sem_publicar
    slugs = [args.slug] if args.slug else None

    with trava_vigia() as Adquirida:
        if not Adquirida:
            log("outro vigia já está rodando — nada a fazer", args.silencioso)
            sys.exit(0)

        if args.loop:
            laco(args.interval, slugs, args.silencioso, args.dry_run, publicar)
            return

        sucesso = verificar_todas(slugs, args.silencioso, args.dry_run, publicar)
    sys.exit(0 if sucesso else 1)


if __name__ == "__main__":
    main()
