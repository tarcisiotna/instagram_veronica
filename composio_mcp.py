"""Acesso ao MCP do Composio (Gmail e Instagram).

Concentra a chave, o protocolo SSE/JSON-RPC e a execução de tools. É usado
tanto pelo vigia de aprovação (leitura do Gmail) quanto pelo publicador
(Instagram), sem que um módulo precise importar o outro.

A chave vem de `COMPOSIO_MCP_KEY` ou do MCP configurado no OpenCode.
"""

import json
import os
import urllib.request
from pathlib import Path

MCP_URL = "https://connect.composio.dev/mcp"
CONFIG_OPENCODE = Path.home() / ".config" / "opencode" / "opencode.json"

_ID_RPC = 0


class ErroFerramenta(RuntimeError):
    """Falha devolvida por uma tool do Composio (não é erro de transporte)."""

    def __init__(self, ferramenta, mensagem, dados=None):
        super().__init__(f"{ferramenta}: {mensagem}")
        self.ferramenta = ferramenta
        self.mensagem = mensagem
        self.dados = dados or {}


def chave_mcp():
    """Chave do MCP: ambiente primeiro, depois a config do OpenCode."""
    chave = os.environ.get("COMPOSIO_MCP_KEY", "").strip()
    if chave:
        return chave
    try:
        config = json.loads(CONFIG_OPENCODE.read_text(encoding="utf-8"))
        return config["mcp"]["servers"]["composio"]["headers"]["x-consumer-api-key"].strip()
    except (OSError, ValueError, KeyError, AttributeError):
        raise SystemExit(
            "❌ Chave do Composio não encontrada.\n"
            "   Defina COMPOSIO_MCP_KEY ou configure o MCP 'composio' em "
            f"{CONFIG_OPENCODE}."
        )


def _json_da_resposta(bruto):
    """O MCP responde em SSE; o JSON útil está no último `data:`."""
    if bruto.lstrip().startswith("{"):
        try:
            return json.loads(bruto)
        except json.JSONDecodeError:
            pass
    ultimo = None
    for linha in bruto.splitlines():
        if not linha.startswith("data:"):
            continue
        pedaco = linha[5:].strip()
        if not pedaco or pedaco == "[DONE]":
            continue
        try:
            ultimo = json.loads(pedaco)
        except json.JSONDecodeError:
            continue
    if ultimo is None:
        raise RuntimeError("resposta do MCP sem JSON")
    return ultimo


def _rpc(payload, timeout=120):
    headers = {
        "x-consumer-api-key": chave_mcp(),
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    requisicao = urllib.request.Request(
        MCP_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(requisicao, timeout=timeout) as resposta:
        bruto = resposta.read().decode("utf-8", "replace")
    return _json_da_resposta(bruto)


def chamar_mcp(nome, argumentos, timeout=120, verificar_sucesso=True):
    """Chama uma tool do MCP e devolve o `data` da resposta.

    `verificar_sucesso=False` é usado pelo executor de tools: quando uma tool
    interna falha, o Composio devolve `successful=false`, mas ainda assim traz
    o detalhe do erro em `data.results` — que é o que interessa.
    """
    global _ID_RPC
    _ID_RPC += 1
    resposta = _rpc(
        {
            "jsonrpc": "2.0",
            "id": _ID_RPC,
            "method": "tools/call",
            "params": {"name": nome, "arguments": argumentos},
        },
        timeout=timeout,
    )
    if resposta.get("error"):
        raise RuntimeError(f"MCP: {resposta['error'].get('message', 'erro')}")

    conteudo = (resposta.get("result") or {}).get("content") or []
    texto = next((c.get("text") for c in conteudo if c.get("type") == "text"), None)
    if not texto:
        raise RuntimeError("MCP: resposta sem conteúdo")

    interno = json.loads(texto)
    if verificar_sucesso and (
        interno.get("error") or not interno.get("successful", True)
    ):
        detalhe = interno.get("error") or interno
        raise RuntimeError(f"Composio: {json.dumps(detalhe, ensure_ascii=False)[:300]}")
    return interno.get("data") or {}

