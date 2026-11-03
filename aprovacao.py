"""Fluxo de aprovação por e-mail antes de publicar no Instagram.

O carrossel é montado e exportado localmente. Este script sobe os slides para
hospedagem pública (catbox.moe), guarda tudo num arquivo de estado em
`aprovacoes/<slug>.json` e gera o HTML do e-mail de aprovação.

Nada é enviado ao Instagram nesta etapa. Os containers só são criados depois
que a Verônica responde o e-mail com APROVAR — assim o prazo de 24h do
Instagram nunca é estourado.

Uso:
    python3 aprovacao.py preparar perda-peso-onco
    python3 aprovacao.py listar
    python3 aprovacao.py ver perda-peso-onco
    python3 aprovacao.py marcar perda-peso-onco aprovado --message-id 18f...
    python3 aprovacao.py publicar perda-peso-onco --media-id 179... --permalink https://...
"""

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
APROV_DIR = BASE_DIR / "aprovacoes"
SLIDES_ROOT = BASE_DIR / "slides"
POSTS_ROOT = BASE_DIR / "posts"
CATBOX_URL = "https://catbox.moe/user/api.php"

# Hospedagem pública das mídias: o repositório GitHub precisa estar PÚBLICO
# para o Gmail (proxy de imagens) e o Instagram baixarem os arquivos.
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/tarcisiotna/instagram_veronica"
GITHUB_BRANCH = "master"
MEDIA_DIR = BASE_DIR / "publicado"

# Remote esperado: protege contra subir a mídia para um repositório
# inesperado (fork, repositório pessoal, URL errada no `origin`).
GITHUB_REMOTE_ESPERADO = os.environ.get(
    "GITHUB_REMOTE_ESPERADO", "git@github.com:tarcisiotna/instagram_veronica.git"
).strip()

# Enviar a mídia para o catbox (host público de terceiros) só com autorização
# explícita: o arquivo fica disponível num serviço que não controlamos.
ALLOW_CATBOX = os.environ.get("APROVACAO_ALLOW_CATBOX", "").strip().lower() in (
    "1",
    "true",
    "sim",
    "yes",
)

EMAIL_DESTINO_PADRAO = "veronicabomfim.nutri@gmail.com"
# O e-mail de aprovação só pode ir para a conta da proprietária — e só a
# resposta dela vale como aprovação (ver `vigia_aprovacao.py`).
EMAIL_DONO = os.environ.get("APROVACAO_EMAIL", EMAIL_DESTINO_PADRAO).strip().lower()
HANDLE = "@veronicabomfim.nutri"

# Hosts de mídia aceitos. O e-mail de aprovação carrega as imagens direto no
# cliente de e-mail: se a URL apontasse para um host de terceiro, o e-mail
# viraria um rastreador (e a publicação usaria uma imagem não aprovada).
HOSTS_MIDIA_PERMITIDOS = {
    "raw.githubusercontent.com",
    "catbox.moe",
    "files.catbox.moe",
    "litter.catbox.moe",
}

# Slug seguro: usado para montar caminhos e nomes de arquivo.
RE_SLUG = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")
# IDs do Gmail são hexadecimais.
RE_ID_GMAIL = re.compile(r"^[0-9a-f]{8,40}$")

BRAND_PRIMARY = "#bf9566"
BRAND_DARK = "#394233"
BRAND_LIGHT = "#ecd7ba"
LIGHT_BG = "#FAF9F7"

STATUS_VALIDOS = ["pendente", "aprovado", "rejeitado", "publicado", "cancelado"]


# --------------------------------------------------------------- utilidades


def agora():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def url_midia_valida(url):
    """True se a URL é https e o host é um dos hosts de mídia do projeto."""
    if not isinstance(url, str) or not url.lower().startswith("https://"):
        return False
    partes = url.split("/")
    if len(partes) < 4:
        return False
    host = partes[2].split("@")[-1].split(":")[0].lower()
    return host in HOSTS_MIDIA_PERMITIDOS


def slug_valido(slug):
    """True se o slug pode virar caminho/nome de arquivo com segurança."""
    return bool(RE_SLUG.match(slug or "")) and ".." not in slug


def _exigir_slug(slug):
    if not slug_valido(slug):
        raise SystemExit(
            f"❌ Slug inválido: '{slug}'\n"
            "   Use apenas letras, números, ponto, hífen e underscore "
            "(máx. 80 caracteres)."
        )
    return slug


def arquivo_estado(slug):
    return APROV_DIR / f"{slug}.json"


def carregar(slug):
    if not slug_valido(slug):
        return None
    caminho = arquivo_estado(slug)
    if not caminho.exists():
        return None
    return json.loads(caminho.read_text(encoding="utf-8"))


def salvar(dados):
    slug = _exigir_slug(dados["slug"])
    APROV_DIR.mkdir(parents=True, exist_ok=True)
    caminho = arquivo_estado(slug)
    caminho.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return caminho


def registrar_evento(dados, evento, detalhe=""):
    dados.setdefault("historico", []).append(
        {"em": agora(), "evento": evento, "detalhe": detalhe}
    )


def slides_do_tema(slug):
    pasta = SLIDES_ROOT / _exigir_slug(slug)
    if not pasta.is_dir():
        raise SystemExit(f"❌ Pasta não encontrada: {pasta}")
    arquivos = list(pasta.glob("slide_*.png"))
    if not arquivos:
        raise SystemExit(f"❌ Nenhum slide_*.png em {pasta}")

    def numero(p):
        m = re.search(r"slide_(\d+)\.png$", p.name)
        return int(m.group(1)) if m else 0

    return sorted(arquivos, key=numero)


def midia_do_tema(slug):
    """Detecta se o tema é carrossel (slides/) ou post único (posts/).

    Retorna (lista_de_imagens, tipo) onde tipo é "carousel" ou "post".
    Para carrossel: lista de slide_*.png ordenada.
    Para post único: lista com um único post.png.
    """
    slug = _exigir_slug(slug)

    # 1. Tenta carrossel
    pasta_slides = SLIDES_ROOT / slug
    if pasta_slides.is_dir():
        arquivos = list(pasta_slides.glob("slide_*.png"))
        if arquivos:

            def numero(p):
                m = re.search(r"slide_(\d+)\.png$", p.name)
                return int(m.group(1)) if m else 0

            return sorted(arquivos, key=numero), "carousel"

    # 2. Tenta post único
    pasta_post = POSTS_ROOT / slug
    if pasta_post.is_dir():
        post_png = pasta_post / "post.png"
        if post_png.exists():
            return [post_png], "post"

    raise SystemExit(
        f"❌ Nenhuma mídia encontrada para '{slug}' "
        f"(esperado slides/{slug}/slide_*.png ou posts/{slug}/post.png)"
    )


def _git(*args, timeout=120):
    """Executa um comando git no repositório do projeto."""
    return subprocess.run(
        ["git", "-C", str(BASE_DIR), *args],
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def _remote_confere():
    """Confere que o `origin` é o repositório esperado antes de versionar mídia.

    `upload_github` faz commit + push automático. Sem esta checagem, um remote
    apontando para outro repositório (ou uma URL digitada errado) publica a
    mídia do cliente em um lugar que ninguém revisou.
    """
    remoto = _git("remote", "get-url", "origin")
    if remoto.returncode != 0:
        raise RuntimeError("remote 'origin' não configurado")
    atual = (remoto.stdout or "").strip()
    if atual != GITHUB_REMOTE_ESPERADO:
        raise RuntimeError(
            f"remote 'origin' inesperado: '{atual}' (esperado '{GITHUB_REMOTE_ESPERADO}'). "
            "Defina GITHUB_REMOTE_ESPERADO para confirmar outro repositório."
        )
    return atual


def upload_github(caminho, slug, branch=GITHUB_BRANCH):
    """Publica a mídia no repositório GitHub público e devolve a URL raw.

    O arquivo é copiado para `publicado/<slug>/`, versionado e enviado para o
    GitHub. A URL raw serve o arquivo para o Gmail e para o Instagram.
    """
    _remote_confere()
    destino_dir = MEDIA_DIR / slug
    destino_dir.mkdir(parents=True, exist_ok=True)
    destino = destino_dir / caminho.name
    shutil.copy2(caminho, destino)
    rel = destino.relative_to(BASE_DIR).as_posix()

    add = _git("add", "--", rel)
    if add.returncode != 0:
        raise RuntimeError(f"git add falhou: {add.stderr.strip()}")

    status = _git("status", "--porcelain", "--", rel)
    if status.stdout.strip():
        commit = _git("commit", "-m", f"midia: {slug}/{caminho.name}", "--", rel)
        if commit.returncode != 0:
            raise RuntimeError(
                f"git commit falhou: {commit.stderr.strip() or commit.stdout.strip()}"
            )

    push = _git("push", "origin", branch)
    if push.returncode != 0:
        raise RuntimeError(f"git push falhou: {push.stderr.strip()}")

    return f"{GITHUB_RAW_BASE}/{branch}/{rel}"


def upload_catbox(caminho, tentativas=3):
    """Sobe um arquivo para o catbox.moe e devolve a URL pública (fallback)."""
    erro = None
    for _ in range(tentativas):
        try:
            saida = subprocess.run(
                [
                    "curl",
                    "-s",
                    "-m",
                    "90",
                    "-F",
                    "reqtype=fileupload",
                    "-F",
                    f"fileToUpload=@{caminho}",
                    CATBOX_URL,
                ],
                capture_output=True,
                text=True,
                timeout=120,
            )
            url = (saida.stdout or "").strip()
            if url.startswith("https://"):
                return url
            erro = url or saida.stderr.strip()
        except Exception as exc:  # noqa: BLE001
            erro = str(exc)
    raise RuntimeError(f"Falha ao subir {caminho.name}: {erro}")


def validar_url_publica(url, tentativas=5, espera=4):
    """Confere se a URL pública devolve conteúdo (protege contra arquivo vazio)."""
    erro = None
    for _ in range(tentativas):
        try:
            saida = subprocess.run(
                [
                    "curl",
                    "-s",
                    "-L",
                    "-o",
                    "/dev/null",
                    "-w",
                    "%{http_code} %{size_download}",
                    "-m",
                    "60",
                    url,
                ],
                capture_output=True,
                text=True,
                timeout=90,
            )
            partes = (saida.stdout or "").split()
            codigo = partes[0] if partes else "000"
            tamanho = int(partes[1]) if len(partes) > 1 else 0
            if codigo == "200" and tamanho > 0:
                return True
            erro = f"HTTP {codigo}, {tamanho} bytes"
        except Exception as exc:  # noqa: BLE001
            erro = str(exc)
        time.sleep(espera)
    raise RuntimeError(f"URL pública não devolve imagem ({erro}): {url}")


def upload_publico(caminho, slug):
    """Publica a mídia e devolve a URL pública.

    Ordem: GitHub (principal) -> catbox (fallback, só com
    `APROVACAO_ALLOW_CATBOX=1`, porque é um host público de terceiros). Em
    ambos os casos a URL é validada: se o host devolver arquivo vazio, a
    publicação é considerada falha em vez de gerar link quebrado.
    """
    erros = []

    try:
        url = upload_github(caminho, slug)
        validar_url_publica(url)
        return url
    except Exception as exc:  # noqa: BLE001
        erros.append(f"GitHub: {exc}")
        print(f"⚠️  GitHub indisponível ({exc}) — trying catbox...")

    if not ALLOW_CATBOX:
        raise SystemExit(
            "❌ Não foi possível publicar a mídia no GitHub:\n  - "
            + "\n  - ".join(erros)
            + "\n\nO fallback catbox.moe fica desligado por padrão (host público "
            "de terceiros).\nPara liberar: APROVACAO_ALLOW_CATBOX=1"
        )

    try:
        url = upload_catbox(caminho)
        validar_url_publica(url)
        return url
    except Exception as exc:  # noqa: BLE001
        erros.append(f"catbox: {exc}")

    raise SystemExit(
        "❌ Não foi possível publicar a mídia em nenhum host:\n  - "
        + "\n  - ".join(erros)
    )



def extrair_titulo(legenda):
    for linha in legenda.splitlines():
        limpa = linha.strip()
        if not limpa:
            continue
        if limpa.startswith("📷") or limpa.startswith("@"):
            continue
        return limpa
    return "Novo carrossel"


def extrair_legenda_instagram(legenda):
    """Remove o cabeçalho de exibição e devolve o texto que vai no Instagram."""
    linhas = legenda.splitlines()
    while linhas:
        primeira = linhas[0].strip()
        if primeira and not primeira.startswith(("📷", "@")):
            break
        linhas.pop(0)
    return "\n".join(linhas).strip()


# ------------------------------------------------------------- html do e-mail


def gerar_html_email(dados):
    """HTML do e-mail de aprovação.

    Tudo que vem do arquivo de estado (título, URLs, legenda, slug) passa por
    `html.escape`: sem isso, um texto malicioso na legenda/título conseguiria
    injetar HTML no e-mail de aprovação e alterar as instruções que a
    proprietária lê antes de aprovar.
    """
    imagens = dados["imagens"]
    total = len(imagens)
    tipo = dados.get("tipo", "carousel")

    invalidas = [u for u in imagens if not url_midia_valida(u)]
    if invalidas:
        raise SystemExit(
            "❌ URL de mídia fora dos hosts permitidos: "
            + ", ".join(str(u) for u in invalidas)
            + "\n   Só são aceitas URLs https de raw.githubusercontent.com "
            "(ou catbox, se o fallback estiver ligado)."
        )

    blocos = []
    for i, url in enumerate(imagens, start=1):
        if total == 1:
            rotulo = "Post"
        else:
            rotulo = "CTA" if i == total else f"Slide {i}"
        url_segura = html.escape(url, quote=True)
        rotulo_seguro = html.escape(rotulo, quote=True)
        blocos.append(
            f'<td width="50%" style="padding:6px;vertical-align:top;">'
            f'<div style="font:600 11px Arial,sans-serif;color:#8A8580;'
            f'letter-spacing:1.5px;text-transform:uppercase;padding:0 0 6px 2px;">{rotulo_seguro}</div>'
            f'<a href="{url_segura}" style="text-decoration:none;">'
            f'<img src="{url_segura}" width="260" alt="{rotulo_seguro}" '
            f'style="display:block;width:100%;max-width:260px;border-radius:10px;'
            f'border:1px solid #e6e1d8;"></a></td>'
        )
    linhas = []
    for i in range(0, len(blocos), 2):
        linhas.append("<tr>" + "".join(blocos[i : i + 2]) + "</tr>")
    galeria = "".join(linhas)

    legenda = html.escape(extrair_legenda_instagram(dados["legenda"]))
    hashtags = len(re.findall(r"#\w+", dados["legenda"]))
    unidade = "post" if tipo == "post" else "slides"
    contagem = f"{total} {unidade}"
    titulo = html.escape(dados["titulo"])
    slug = html.escape(dados["slug"])
    criado_em = html.escape(dados["criado_em"])

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<body style="margin:0;padding:0;background:#f2efe9;">
<div style="max-width:640px;margin:0 auto;background:#ffffff;font-family:Arial,Helvetica,sans-serif;">

  <div style="background:{BRAND_DARK};padding:28px 32px;">
    <div style="font:600 10px Arial,sans-serif;letter-spacing:2.5px;color:{BRAND_LIGHT};text-transform:uppercase;padding-bottom:10px;">
      Aprovação de conteúdo
    </div>
    <div style="font:700 22px Georgia,'Times New Roman',serif;color:#ffffff;line-height:1.3;">
      {titulo}
    </div>
    <div style="font:400 12px Arial,sans-serif;color:rgba(255,255,255,0.65);padding-top:10px;">
      {HANDLE} &nbsp;·&nbsp; {contagem} &nbsp;·&nbsp; {len(dados['legenda'])} caracteres de legenda &nbsp;·&nbsp; {hashtags} hashtags
    </div>
  </div>

  <div style="padding:22px 32px 4px;">
    <div style="background:{LIGHT_BG};border-left:3px solid {BRAND_PRIMARY};padding:14px 16px;border-radius:4px;">
      <div style="font:400 13px Arial,sans-serif;color:#4a4a44;line-height:1.6;">
        <strong style="color:{BRAND_DARK};">Nada foi publicado ainda.</strong>
        O post só vai para o Instagram depois da sua resposta a este e-mail.
      </div>
    </div>
  </div>

  <div style="padding:18px 26px 6px;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0">{galeria}</table>
  </div>

  <div style="padding:14px 32px 8px;">
    <div style="font:600 10px Arial,sans-serif;letter-spacing:2px;color:{BRAND_PRIMARY};text-transform:uppercase;padding-bottom:10px;">
      Legenda do post
    </div>
    <div style="background:#faf9f7;border:1px solid #e6e1d8;border-radius:8px;padding:16px;font:400 12.5px/1.65 Arial,sans-serif;color:#4a4a44;white-space:pre-wrap;">{legenda}</div>
  </div>

  <div style="padding:22px 32px 30px;">
    <div style="font:600 10px Arial,sans-serif;letter-spacing:2px;color:{BRAND_PRIMARY};text-transform:uppercase;padding-bottom:12px;">
      Como responder
    </div>
    <table width="100%" cellpadding="0" cellspacing="0" border="0">
      <tr>
        <td width="50%" style="padding-right:6px;">
          <div style="background:#eef3ea;border:1px solid #cfe0c4;border-radius:8px;padding:14px 16px;">
            <div style="font:700 13px Arial,sans-serif;color:#3d5c2f;padding-bottom:4px;">APROVAR</div>
            <div style="font:400 12px Arial,sans-serif;color:#5d6b55;line-height:1.5;">Responda só com a palavra <strong>APROVAR</strong> para publicar.</div>
          </div>
        </td>
        <td width="50%" style="padding-left:6px;">
          <div style="background:#fbf0ee;border:1px solid #eccfc8;border-radius:8px;padding:14px 16px;">
            <div style="font:700 13px Arial,sans-serif;color:#8a3b2c;padding-bottom:4px;">REJEITAR</div>
            <div style="font:400 12px Arial,sans-serif;color:#7d5b53;line-height:1.5;">Responda <strong>REJEITAR</strong> + o que corrigir. Nada é publicado.</div>
          </div>
        </td>
      </tr>
    </table>
    <div style="font:400 11.5px Arial,sans-serif;color:#8A8580;line-height:1.6;padding-top:14px;">
      O e-mail é o único canal de aprovação. Qualquer outra resposta deixa o post em espera.
    </div>
  </div>

  <div style="background:#faf9f7;border-top:1px solid #e6e1d8;padding:18px 32px;">
    <div style="font:400 11px Arial,sans-serif;color:#8A8580;line-height:1.7;">
      Referência interna: <code style="color:#4a4a44;">{slug}</code><br>
      Preparado em {criado_em}
    </div>
  </div>

</div>
</body>
</html>"""


# ----------------------------------------------------------------- comandos


def _destino_de_aprovacao(args, dados):
    """E-mail que recebe a aprovação.

    Só a conta da proprietária pode receber e responder a aprovação: se o
    e-mail de aprovação fosse enviado para um endereço controlado por outra
    pessoa, essa pessoa aprovaria o post sozinha.
    """
    destino = (
        args.para
        or (dados.get("email") or {}).get("para")
        or EMAIL_DESTINO_PADRAO
    ).strip()
    if destino.lower() != EMAIL_DONO:
        raise SystemExit(
            f"❌ O e-mail de aprovação precisa ir para '{EMAIL_DONO}' "
            f"(recebido: '{destino}').\n"
            "   Só a resposta dessa conta vale como aprovação — o vigia "
            "descarta respostas de outros remetentes.\n"
            "   Para outro fluxo, ajuste APROVACAO_EMAIL no ambiente."
        )
    return destino


def cmd_preparar(args):
    slug = _exigir_slug(args.slug)
    legenda_path = POSTS_ROOT / slug / "legenda.txt"
    slides_legenda_path = SLIDES_ROOT / slug / "legenda.txt"

    # Escolhe a legenda: posts/ primeiro (post único), depois slides/ (carrossel)
    if legenda_path.exists():
        pasta_midia = POSTS_ROOT / slug
        legenda = legenda_path.read_text(encoding="utf-8")
    elif slides_legenda_path.exists():
        pasta_midia = SLIDES_ROOT / slug
        legenda = slides_legenda_path.read_text(encoding="utf-8")
    else:
        raise SystemExit(f"❌ Legenda não encontrada para '{slug}'")

    midia, tipo = midia_do_tema(slug)
    total = len(midia)

    dados = carregar(slug) or {}

    # Valida o destino ANTES de qualquer upload: se o e-mail de aprovação for
    # para um endereço que não é o da proprietária, nada deve ser publicado.
    destino = _destino_de_aprovacao(args, dados)

    dados.update(
        {
            "slug": slug,
            "tipo": tipo,
            "titulo": args.titulo or extrair_titulo(legenda),
            "legenda": legenda,
            "slides_dir": str(pasta_midia.relative_to(BASE_DIR)),
            "total_slides": total,
        }
    )
    dados.setdefault("criado_em", agora())

    urls_antigas = dados.get("imagens") or []
    reutilizar = len(urls_antigas) == total and not args.reupload

    if reutilizar:
        dados["imagens"] = urls_antigas
        print(f"♻️  Reaproveitando {len(urls_antigas)} URLs já enviadas")
    else:
        urls = []
        for i, slide in enumerate(midia, start=1):
            print(f"⬆️  {tipo} {i}/{total}: {slide.name} ... ", end="", flush=True)
            url = upload_publico(slide, slug)
            print(url)
            urls.append(url)
        dados["imagens"] = urls

    dados["status"] = "pendente"
    dados.setdefault("email", {})
    dados["email"]["para"] = destino
    dados["email"]["assunto"] = f"[Aprovação] {dados['titulo']}"
    registrar_evento(dados, "preparado", f"{total} {tipo}(s) enviados para hospedagem")

    caminho = salvar(dados)

    html_path = APROV_DIR / f"{slug}-email.html"
    html_path.write_text(gerar_html_email(dados), encoding="utf-8")

    print()
    print(f"✅ Estado salvo em {caminho.relative_to(BASE_DIR)}")
    print(f"📧 HTML do e-mail: {html_path.relative_to(BASE_DIR)}")
    print(f"📬 Destino: {dados['email']['para']}")
    print(f"🏷️  Assunto: {dados['email']['assunto']}")
    print(f"📊 Status: {dados['status']}")
    print(f"📁 Tipo: {tipo}")
    print()
    print("Próximo passo: enviar o e-mail via Gmail com o HTML acima,")
    print("depois rodar:  python3 aprovacao.py marcar %s pendente --thread-id <id>" % slug)


def cmd_listar(args):
    APROV_DIR.mkdir(parents=True, exist_ok=True)
    arquivos = sorted(APROV_DIR.glob("*.json"))
    if not arquivos:
        print("Nenhuma aprovação registrada.")
        return
    for caminho in arquivos:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        print(
            f"{dados['status']:<10} {dados['slug']:<28} "
            f"{dados.get('total_slides', '?')} slides  "
            f"criado {dados.get('criado_em', '?')}"
        )


def cmd_ver(args):
    slug = _exigir_slug(args.slug)
    dados = carregar(slug)
    if not dados:
        raise SystemExit(f"❌ Nenhuma aprovação para '{slug}'")
    resumo = {k: v for k, v in dados.items() if k != "legenda"}
    print(json.dumps(resumo, ensure_ascii=False, indent=2))
    print(f"\n--- legenda ({len(dados['legenda'])} caracteres) ---")
    print(dados["legenda"])


def cmd_marcar(args):
    slug = _exigir_slug(args.slug)
    dados = carregar(slug)
    if not dados:
        raise SystemExit(f"❌ Nenhuma aprovação para '{slug}'")
    if args.status not in STATUS_VALIDOS:
        raise SystemExit(f"❌ Status inválido. Use: {', '.join(STATUS_VALIDOS)}")

    anterior = dados["status"]
    dados["status"] = args.status
    dados.setdefault("email", {})
    if args.message_id:
        if not RE_ID_GMAIL.match(args.message_id.strip().lower()):
            raise SystemExit(
                f"❌ message_id inválido: '{args.message_id}' "
                "(esperado ID hexadecimal do Gmail)."
            )
        dados["email"]["message_id"] = args.message_id.strip().lower()
    if args.thread_id:
        if not RE_ID_GMAIL.match(args.thread_id.strip().lower()):
            raise SystemExit(
                f"❌ thread_id inválido: '{args.thread_id}' "
                "(esperado ID hexadecimal do Gmail)."
            )
        dados["email"]["thread_id"] = args.thread_id.strip().lower()
    if args.status == "aprovado":
        dados["aprovado_em"] = agora()
    registrar_evento(dados, "status", f"{anterior} → {args.status} {args.detalhe or ''}".strip())
    salvar(dados)
    print(f"✅ {slug}: {anterior} → {args.status}")


def cmd_publicar(args):
    slug = _exigir_slug(args.slug)
    dados = carregar(slug)
    if not dados:
        raise SystemExit(f"❌ Nenhuma aprovação para '{slug}'")
    if dados["status"] not in ("aprovado", "publicado"):
        raise SystemExit(
            f"❌ Status atual é '{dados['status']}'. Só publica depois de 'aprovado'."
        )
    if args.permalink and not args.permalink.startswith("https://"):
        raise SystemExit(
            f"❌ Permalink inválido: '{args.permalink}' (deve começar com https://)."
        )
    dados["status"] = "publicado"
    dados["publicacao"] = {
        "media_id": args.media_id,
        "permalink": args.permalink,
        "publicado_em": agora(),
    }
    registrar_evento(dados, "publicado", args.permalink or "")
    salvar(dados)
    print(f"✅ {slug} publicado: {args.permalink}")


def main():
    parser = argparse.ArgumentParser(description="Aprovação por e-mail antes de publicar")
    sub = parser.add_subparsers(dest="comando", required=True)

    p = sub.add_parser("preparar", help="sobe os slides e gera o e-mail de aprovação")
    p.add_argument("slug")
    p.add_argument("--para", help="e-mail de destino")
    p.add_argument("--titulo", help="título exibido no assunto")
    p.add_argument("--reupload", action="store_true", help="reenvia as imagens mesmo se já houver URL")
    p.set_defaults(func=cmd_preparar)

    p = sub.add_parser("listar", help="lista aprovações")
    p.set_defaults(func=cmd_listar)

    p = sub.add_parser("ver", help="mostra uma aprovação")
    p.add_argument("slug")
    p.set_defaults(func=cmd_ver)

    p = sub.add_parser("marcar", help="atualiza o status de uma aprovação")
    p.add_argument("slug")
    p.add_argument("status")
    p.add_argument("--message-id")
    p.add_argument("--thread-id")
    p.add_argument("--detalhe")
    p.set_defaults(func=cmd_marcar)

    p = sub.add_parser("publicar", help="registra a publicação")
    p.add_argument("slug")
    p.add_argument("--media-id", required=True)
    p.add_argument("--permalink")
    p.set_defaults(func=cmd_publicar)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
