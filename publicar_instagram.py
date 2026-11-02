#!/usr/bin/env python3
"""Publica no Instagram um post ou carrossel já aprovado por e-mail.

Só é chamado depois que o vigia encontrou um `APROVAR` de verdade. Nenhum
container é criado antes disso — o prazo de 24h do Instagram continua
respeitado.

A publicação usa a Graph API direto pelo proxy do Composio
(`COMPOSIO_PROXY_EXECUTE`). As tools prontas de carrossel do Composio recusam
os containers filhos com "Invalid parameter in carousel request"; pela API
conseguimos montar o carrossel com `media_type=CAROUSEL` e `children`.

Fluxo (carrossel):
    1. um container `is_carousel_item` por slide, na ordem
    2. espera todos ficarem FINISHED
    3. container pai com a legenda aprovada
    4. espera o pai ficar FINISHED
    5. publish do container pai
    6. leitura do permalink

Post único usa o mesmo caminho, sem os containers filhos.

Uso manual (normalmente não é necessário):
    python3 publicar_instagram.py <slug>
    python3 publicar_instagram.py <slug> --dry-run
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta

from aprovacao import agora, carregar, extrair_legenda_instagram
from composio_mcp import ErroFerramenta, chamar_mcp

IG_USER_ID = os.environ.get("IG_USER_ID", "28882452441414713").strip()
GRAPH_VERSION = os.environ.get("IG_GRAPH_VERSION", "v21.0").strip().strip("/")

LIMITE_LEGENDA = 2200
LIMITE_HASHTAGS = 30
MAX_ITENS = 10
VALIDADE_CONTAINER = timedelta(hours=23)
ESPERA_FILHOS = 180
ESPERA_PAI = 300
INTERVALO_STATUS = 3

CHAVES_ID = ("id", "creation_id", "container_id", "media_id")


class ErroPublicacao(RuntimeError):
    """Falha ao publicar (validação, API do Instagram ou resposta inesperada)."""


# --------------------------------------------------------------- Graph API


def _mensagem_de_erro(recurso):
    if isinstance(recurso, dict):
        erro = recurso.get("error")
        if isinstance(erro, dict):
            mensagem = erro.get("message") or erro.get("error_user_msg")
            codigo = erro.get("code")
            if mensagem:
                return f"{mensagem} (código {codigo})" if codigo else mensagem
        for chave in ("message", "error", "detail"):
            if recurso.get(chave):
                return str(recurso[chave])
    return json.dumps(recurso, ensure_ascii=False)[:500]


def _graph(metodo, caminho, parametros=None, corpo=None, timeout=180):
    """Chama a Graph API do Instagram pelo proxy do Composio.

    GET usa query string (poucos campos). POST manda JSON no body: a API
    aceita, e assim a legenda longa com quebras de linha e emojis não quebra
    a URL do proxy.
    """
    argumentos = {
        "toolkit_slug": "instagram",
        "endpoint": f"/{GRAPH_VERSION}{caminho}",
        "method": metodo,
    }
    if parametros:
        argumentos["parameters"] = [
            {"name": nome, "value": str(valor), "type": "query"}
            for nome, valor in parametros.items()
        ]
    if corpo is not None:
        argumentos["body"] = corpo

    dados = chamar_mcp("COMPOSIO_PROXY_EXECUTE", argumentos, timeout=timeout)
    status = int(dados.get("status") or 0)
    recurso = dados.get("data")
    if status != 200:
        raise ErroFerramenta("instagram", _mensagem_de_erro(recurso), recurso)
    if not isinstance(recurso, dict):
        raise ErroPublicacao(f"resposta inesperada da Graph API: {recurso!r}"[:500])
    return recurso


def _extrair_id(dados):
    if isinstance(dados, str):
        if dados.strip():
            return dados.strip()
        raise ErroPublicacao("resposta sem id")
    if isinstance(dados, dict):
        for chave in CHAVES_ID:
            valor = dados.get(chave)
            if valor not in (None, ""):
                return str(valor)
        for chave in ("data", "result", "media"):
            if isinstance(dados.get(chave), (dict, list)):
                try:
                    return _extrair_id(dados[chave])
                except ErroPublicacao:
                    continue
    raise ErroPublicacao(f"resposta sem id de criação: {json.dumps(dados)[:300]}")


def _status_container(criacao_id):
    dados = _graph(
        "GET",
        f"/{criacao_id}",
        {"fields": "status_code,status"},
        timeout=120,
    )
    return dados.get("status_code") or dados.get("status")


def _esperar_containers(ids, timeout, intervalo=INTERVALO_STATUS):
    """Espera os containers ficarem FINISHED antes de usá-los."""
    pendentes = list(ids)
    limite = time.monotonic() + timeout
    while pendentes:
        for criacao_id in list(pendentes):
            status = _status_container(criacao_id)
            if status == "FINISHED":
                pendentes.remove(criacao_id)
            elif status in ("ERROR", "EXPIRED"):
                raise ErroPublicacao(
                    f"container {criacao_id} não ficou pronto: {status}"
                )
        if not pendentes:
            return
        if time.monotonic() >= limite:
            raise ErroPublicacao(
                "containers ainda em processamento: " + ", ".join(pendentes)
            )
        time.sleep(intervalo)


# ------------------------------------------------------------------ helpers


def legenda_do_post(dados):
    """Legenda que vai para o Instagram (mesma do e-mail de aprovação)."""
    legenda = extrair_legenda_instagram(dados.get("legenda") or "").strip()
    if not legenda:
        raise ErroPublicacao("legenda vazia")
    if len(legenda) > LIMITE_LEGENDA:
        raise ErroPublicacao(
            f"legenda com {len(legenda)} caracteres (limite {LIMITE_LEGENDA})"
        )
    hashtags = len(re.findall(r"#\w+", legenda))
    if hashtags > LIMITE_HASHTAGS:
        raise ErroPublicacao(
            f"legenda com {hashtags} hashtags (limite {LIMITE_HASHTAGS})"
        )
    return legenda


def _normalizar(texto):
    return re.sub(r"\s+", " ", texto or "").strip().casefold()


def _data_iso(valor):
    if not valor:
        return None
    try:
        return datetime.fromisoformat(str(valor).replace("Z", "+00:00"))
    except ValueError:
        return None


def _container_reutilizavel(publicacao):
    """Container criado numa tentativa anterior e ainda dentro do prazo."""
    criacao_id = publicacao.get("criacao_id")
    if not criacao_id or publicacao.get("fase") not in (
        "container_pronto",
        "publicando",
        "falha_publicacao",
    ):
        return None
    criado = _data_iso(publicacao.get("criacao_em"))
    if not criado:
        return None
    referencia = datetime.now(criado.tzinfo) if criado.tzinfo else datetime.now()
    if referencia - criado >= VALIDADE_CONTAINER:
        return None
    return str(criacao_id)


def _lista_de_media(dados):
    if isinstance(dados, list):
        return dados
    if isinstance(dados, dict):
        for chave in ("data", "media", "items"):
            if isinstance(dados.get(chave), list):
                return dados[chave]
    return []


def _permalink(media_id):
    """Permalink é cosmético: se falhar, a publicação continua válida."""
    try:
        dados = _graph(
            "GET",
            f"/{media_id}",
            {"fields": "id,permalink,media_type,timestamp"},
            timeout=120,
        )
    except Exception:  # noqa: BLE001
        return None
    return dados.get("permalink") if isinstance(dados, dict) else None


def _recuperar_publicacao(legenda, criacao_em):
    """Depois de um erro no publish, confere se o post saiu mesmo assim.

    Evita publicar duas vezes quando a chamada deu timeout/demorou mas o
    Instagram concluiu. Só aceita mídia com a mesma legenda criada depois do
    container.
    """
    try:
        dados = _graph(
            "GET",
            f"/{IG_USER_ID}/media",
            {
                "fields": "id,permalink,caption,timestamp,media_type",
                "limit": "10",
            },
            timeout=120,
        )
    except Exception:  # noqa: BLE001
        return None

    alvo = _normalizar(legenda)[:120]
    desde = _data_iso(criacao_em)
    for item in _lista_de_media(dados):
        if not isinstance(item, dict):
            continue
        if _normalizar(item.get("caption"))[:120] != alvo:
            continue
        quando = _data_iso(item.get("timestamp"))
        if desde and quando and quando < desde - timedelta(minutes=10):
            continue
        return {
            "media_id": str(item.get("id")),
            "permalink": item.get("permalink"),
            "recuperado": True,
        }
    return None


def _progresso(callback, publicacao):
    if callback:
        callback(dict(publicacao))


# ---------------------------------------------------------------- publicação


def publicar(dados, ao_progredir=None):
    """Publica o estado aprovado e devolve o bloco `publicacao`.

    `ao_progredir` é chamado a cada etapa para o chamador persistir o
    progresso (ids dos filhos, container pai) e conseguir continuar de onde
    parou se algo falhar.
    """
    if dados.get("status") == "publicado":
        return dict(dados.get("publicacao") or {})
    if dados.get("status") != "aprovado":
        raise ErroPublicacao(
            f"status '{dados.get('status')}' não permite publicar (precisa ser aprovado)"
        )

    imagens = [url for url in (dados.get("imagens") or []) if url]
    tipo = dados.get("tipo") or ("carousel" if len(imagens) > 1 else "post")
    if tipo == "post":
        if len(imagens) != 1:
            raise ErroPublicacao(f"post único precisa de 1 imagem, tem {len(imagens)}")
    elif not 2 <= len(imagens) <= MAX_ITENS:
        raise ErroPublicacao(
            f"carrossel precisa de 2 a {MAX_ITENS} imagens, tem {len(imagens)}"
        )

    legenda = legenda_do_post(dados)
    anterior = dict(dados.get("publicacao") or {})
    publicacao = {
        "fase": "criando",
        "filhos": list(anterior.get("filhos") or []),
        "iniciado_em": anterior.get("iniciado_em") or agora(),
    }

    criacao_id = _container_reutilizavel(anterior)
    if criacao_id:
        publicacao.update(
            {
                "fase": "container_pronto",
                "criacao_id": criacao_id,
                "criacao_em": anterior.get("criacao_em"),
                "filhos": list(anterior.get("filhos") or []),
            }
        )
    elif tipo == "post":
        dados_container = _graph(
            "POST",
            f"/{IG_USER_ID}/media",
            corpo={"image_url": imagens[0], "caption": legenda},
            timeout=300,
        )
        criacao_id = _extrair_id(dados_container)
        publicacao.update(
            {
                "fase": "container_pronto",
                "criacao_id": criacao_id,
                "criacao_em": agora(),
            }
        )
        _progresso(ao_progredir, publicacao)
    else:
        filhos = []
        for indice, url in enumerate(imagens, start=1):
            dados_filho = _graph(
                "POST",
                f"/{IG_USER_ID}/media",
                corpo={"image_url": url, "is_carousel_item": True},
                timeout=300,
            )
            filhos.append(_extrair_id(dados_filho))
            publicacao.update(
                {"fase": f"filhos {indice}/{len(imagens)}", "filhos": list(filhos)}
            )
            _progresso(ao_progredir, publicacao)

        _esperar_containers(filhos, ESPERA_FILHOS)
        dados_container = _graph(
            "POST",
            f"/{IG_USER_ID}/media",
            corpo={
                "media_type": "CAROUSEL",
                "children": ",".join(filhos),
                "caption": legenda,
            },
            timeout=300,
        )
        criacao_id = _extrair_id(dados_container)
        publicacao.update(
            {
                "fase": "container_pronto",
                "criacao_id": criacao_id,
                "criacao_em": agora(),
                "filhos": list(filhos),
            }
        )
        _progresso(ao_progredir, publicacao)

    _esperar_containers([criacao_id], ESPERA_PAI)

    publicacao["fase"] = "publicando"
    _progresso(ao_progredir, publicacao)

    try:
        dados_publish = _graph(
            "POST",
            f"/{IG_USER_ID}/media_publish",
            corpo={"creation_id": criacao_id},
            timeout=420,
        )
        media_id = _extrair_id(dados_publish)
        recuperado = False
    except ErroFerramenta as erro:
        recuperado_dados = _recuperar_publicacao(legenda, publicacao.get("criacao_em"))
        if not recuperado_dados:
            publicacao["fase"] = "falha_publicacao"
            publicacao["erro"] = str(erro)[:500]
            _progresso(ao_progredir, publicacao)
            raise
        media_id = recuperado_dados["media_id"]
        publicacao["permalink"] = recuperado_dados.get("permalink")
        recuperado = True

    resultado = {
        "fase": "publicado",
        "media_id": media_id,
        "permalink": publicacao.get("permalink") or _permalink(media_id),
        "criacao_id": criacao_id,
        "filhos": list(publicacao.get("filhos") or []),
        "publicado_em": agora(),
        "iniciado_em": publicacao.get("iniciado_em"),
    }
    if recuperado:
        resultado["recuperado"] = True
    return resultado


# --------------------------------------------------------------------- CLI


def main():
    parser = argparse.ArgumentParser(description="Publica um post aprovado no Instagram")
    parser.add_argument("slug")
    parser.add_argument(
        "--dry-run", action="store_true", help="mostra o que faria, sem chamar o Instagram"
    )
    args = parser.parse_args()

    dados = carregar(args.slug)
    if not dados:
        raise SystemExit(f"❌ Nenhuma aprovação para '{args.slug}'")

    if args.dry_run:
        legenda = legenda_do_post(dados)
        imagens = dados.get("imagens") or []
        print(f"{args.slug}: {dados.get('status')} — {len(imagens)} imagem(ns)")
        print(f"legenda: {len(legenda)} caracteres, {legenda.count('#')} hashtags")
        print("nada foi enviado ao Instagram")
        return

    try:
        resultado = publicar(dados)
    except Exception as erro:  # noqa: BLE001
        raise SystemExit(f"❌ {erro}")

    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
