"""Acesso ao MCP do Composio (Gmail e Instagram).

Concentra a chave, o protocolo SSE/JSON-RPC e a execução de tools. É usado
tanto pelo vigia de aprovação (leitura do Gmail) quanto pelo publicador
(Instagram), sem que um módulo precise importar o outro.

A chave vem de `COMPOSIO_MCP_KEY` (ambiente ou `.env` local) ou do MCP
configurado no OpenCode.

Segurança: a chave concede acesso total às contas de Gmail e Instagram. Por
isso o arquivo que a guarda precisa ter permissão restrita ao dono
(`chmod 600`) — o repositório é público e qualquer segredo versionado ou
legível por outros usuários do sistema vira exposição permanente.
"""

import json
import os
import stat
import urllib.request
from pathlib import Path

MCP_URL = "https://connect.composio.dev/mcp"
CONFIG_OPENCODE = Path.home() / ".config" / "opencode" / "opencode.json"
ENV_FILE = Path(__file__).parent / ".env"

_ID_RPC = 0


class ErroFerramenta(RuntimeError):
    """Falha devolvida por uma tool do Composio (não é erro de transporte)."""

    def __init__(self, ferramenta, mensagem, dados=None):
        super().__init__(f"{ferramenta}: {mensagem}")
        self.ferramenta = ferramenta
        self.mensagem = mensagem
        self.dados = dados or {}


def _exigir_permissao_restrita(caminho):
    """Garante que só o dono do arquivo consegue ler a chave.

    A chave do Composio abre o Gmail e o Instagram da conta. Se o arquivo
    estiver legível por grupo/outros usuários da máquina, qualquer processo
    local lê a credencial. Nesse caso o script recusa o uso e explica o
    conserto.
    """
    try:
        modo = caminho.stat().st_mode
    except OSError:
        return
    if not modo & (stat.S_IRWXG | stat.S_IRWXO):
        return
    raise SystemExit(
        "❌ Arquivo de credencial legível por outros usuários.\n"
        f"   Arquivo: {caminho} ({stat.filemode(modo)})\n"
        "   A chave do Composio dá acesso total ao Gmail e ao Instagram.\n"
        f"   Corrija com: chmod 600 {caminho}\n"
        "   Alternativa: defina COMPOSIO_MCP_KEY no ambiente."
    )


def _ler_env(arquivo=ENV_FILE):
    """Lê um `.env` simples (KEY=VALOR) sem depender de python-dotenv.

    O `.env` está no `.gitignore` — nunca versionar. Ele só preenche variáveis
    que ainda não existam no ambiente.
    """
    if not arquivo.exists():
        return {}
    try:
        conteudo = arquivo.read_text(encoding="utf-8")
    except OSError:
        return {}
    valores = {}
    for linha in conteudo.splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, _, valor = linha.partition("=")
        chave = chave.strip()
        valor = valor.strip()
        if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in "\"'":
            valor = valor[1:-1]
        if chave:
            valores[chave] = valor
            os.environ.setdefault(chave, valor)
    return valores


def _chave_do_arquivo_de_config():
    """Lê a chave da config do OpenCode (com checagem de permissão)."""
    try:
        config = json.loads(CONFIG_OPENCODE.read_text(encoding="utf-8"))
        chave = config["mcp"]["servers"]["composio"]["headers"]["x-consumer-api-key"].strip()
    except (OSError, ValueError, KeyError, AttributeError):
        raise SystemExit(
            "❌ Chave do Composio não encontrada.\n"
            "   Defina COMPOSIO_MCP_KEY ou configure o MCP 'composio' em "
            f"{CONFIG_OPENCODE}."
        )
    if not chave:
        raise SystemExit("❌ Chave do Composio vazia em " f"{CONFIG_OPENCODE}.")
    _exigir_permissao_restrita(CONFIG_OPENCODE)
    return chave


def chave_mcp():
    """Chave do MCP: ambiente primeiro, depois `.env`, depois a config do OpenCode."""
    valores = _ler_env()
    for nome in ("COMPOSIO_MCP_KEY", "COMPOSIO_API_KEY"):
        chave = (os.environ.get(nome) or valores.get(nome) or "").strip()
        if chave:
            # Se o valor veio do `.env`, o arquivo precisa estar protegido.
            if chave == (valores.get(nome) or "").strip():
                _exigir_permissao_restrita(ENV_FILE)
            return chave
    return _chave_do_arquivo_de_config()


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

