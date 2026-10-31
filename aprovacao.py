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
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
APROV_DIR = BASE_DIR / "aprovacoes"
SLIDES_ROOT = BASE_DIR / "slides"
CATBOX_URL = "https://catbox.moe/user/api.php"

EMAIL_DESTINO_PADRAO = "veronicabomfim.nutri@gmail.com"
HANDLE = "@veronicabomfim.nutri"

BRAND_PRIMARY = "#bf9566"
BRAND_DARK = "#394233"
BRAND_LIGHT = "#ecd7ba"
LIGHT_BG = "#FAF9F7"

STATUS_VALIDOS = ["pendente", "aprovado", "rejeitado", "publicado", "cancelado"]


# --------------------------------------------------------------- utilidades


def agora():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def arquivo_estado(slug):
    return APROV_DIR / f"{slug}.json"


def carregar(slug):
    caminho = arquivo_estado(slug)
    if not caminho.exists():
        return None
    return json.loads(caminho.read_text(encoding="utf-8"))


def salvar(dados):
    APROV_DIR.mkdir(parents=True, exist_ok=True)
    caminho = arquivo_estado(dados["slug"])
    caminho.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return caminho


def registrar_evento(dados, evento, detalhe=""):
    dados.setdefault("historico", []).append(
        {"em": agora(), "evento": evento, "detalhe": detalhe}
    )


def slides_do_tema(slug):
    pasta = SLIDES_ROOT / slug
    if not pasta.is_dir():
        raise SystemExit(f"❌ Pasta não encontrada: {pasta}")
    arquivos = list(pasta.glob("slide_*.png"))
    if not arquivos:
        raise SystemExit(f"❌ Nenhum slide_*.png em {pasta}")

    def numero(p):
        m = re.search(r"slide_(\d+)\.png$", p.name)
        return int(m.group(1)) if m else 0

    return sorted(arquivos, key=numero)


def upload_catbox(caminho, tentativas=3):
    """Sobe um arquivo para o catbox.moe e devolve a URL pública."""
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
    raise SystemExit(f"❌ Falha ao subir {caminho.name}: {erro}")


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
    imagens = dados["imagens"]
    total = len(imagens)

    blocos = []
    for i, url in enumerate(imagens, start=1):
        rotulo = "CTA" if i == total else f"Slide {i}"
        blocos.append(
            f'<td width="50%" style="padding:6px;vertical-align:top;">'
            f'<div style="font:600 11px Arial,sans-serif;color:#8A8580;'
            f'letter-spacing:1.5px;text-transform:uppercase;padding:0 0 6px 2px;">{rotulo}</div>'
            f'<a href="{url}" style="text-decoration:none;">'
            f'<img src="{url}" width="260" alt="{rotulo}" '
            f'style="display:block;width:100%;max-width:260px;border-radius:10px;'
            f'border:1px solid #e6e1d8;"></a></td>'
        )
    linhas = []
    for i in range(0, len(blocos), 2):
        linhas.append("<tr>" + "".join(blocos[i : i + 2]) + "</tr>")
    galeria = "".join(linhas)

    legenda = extrair_legenda_instagram(dados["legenda"]).replace("<", "&lt;")
    hashtags = len(re.findall(r"#\w+", dados["legenda"]))

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<body style="margin:0;padding:0;background:#f2efe9;">
<div style="max-width:640px;margin:0 auto;background:#ffffff;font-family:Arial,Helvetica,sans-serif;">

  <div style="background:{BRAND_DARK};padding:28px 32px;">
    <div style="font:600 10px Arial,sans-serif;letter-spacing:2.5px;color:{BRAND_LIGHT};text-transform:uppercase;padding-bottom:10px;">
      Aprovação de conteúdo
    </div>
    <div style="font:700 22px Georgia,'Times New Roman',serif;color:#ffffff;line-height:1.3;">
      {dados['titulo']}
    </div>
    <div style="font:400 12px Arial,sans-serif;color:rgba(255,255,255,0.65);padding-top:10px;">
      {HANDLE} &nbsp;·&nbsp; {total} slides &nbsp;·&nbsp; {len(dados['legenda'])} caracteres de legenda &nbsp;·&nbsp; {hashtags} hashtags
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
      Referência interna: <code style="color:#4a4a44;">{dados['slug']}</code><br>
      Preparado em {dados['criado_em']}
    </div>
  </div>

</div>
</body>
</html>"""


# ----------------------------------------------------------------- comandos


def cmd_preparar(args):
    slug = args.slug
    pasta = SLIDES_ROOT / slug
    legenda_path = pasta / "legenda.txt"
    if not legenda_path.exists():
        raise SystemExit(f"❌ Legenda não encontrada: {legenda_path}")

    slides = slides_do_tema(slug)
    legenda = legenda_path.read_text(encoding="utf-8")

    dados = carregar(slug) or {}
    dados.update(
        {
            "slug": slug,
            "titulo": args.titulo or extrair_titulo(legenda),
            "legenda": legenda,
            "slides_dir": str(pasta.relative_to(BASE_DIR)),
            "total_slides": len(slides),
        }
    )
    dados.setdefault("criado_em", agora())

    urls_antigas = dados.get("imagens") or []
    reutilizar = len(urls_antigas) == len(slides) and not args.reupload

    if reutilizar:
        dados["imagens"] = urls_antigas
        print(f"♻️  Reaproveitando {len(urls_antigas)} URLs já enviadas")
    else:
        urls = []
        for i, slide in enumerate(slides, start=1):
            print(f"⬆️  slide {i}/{len(slides)}: {slide.name} ... ", end="", flush=True)
            url = upload_catbox(slide)
            print(url)
            urls.append(url)
        dados["imagens"] = urls

    dados["status"] = "pendente"
    dados.setdefault("email", {})
    dados["email"]["para"] = args.para or dados["email"].get("para") or EMAIL_DESTINO_PADRAO
    dados["email"]["assunto"] = f"[Aprovação] {dados['titulo']}"
    registrar_evento(dados, "preparado", f"{len(slides)} slides enviados para hospedagem")

    caminho = salvar(dados)

    html_path = APROV_DIR / f"{slug}-email.html"
    html_path.write_text(gerar_html_email(dados), encoding="utf-8")

    print()
    print(f"✅ Estado salvo em {caminho.relative_to(BASE_DIR)}")
    print(f"📧 HTML do e-mail: {html_path.relative_to(BASE_DIR)}")
    print(f"📬 Destino: {dados['email']['para']}")
    print(f"🏷️  Assunto: {dados['email']['assunto']}")
    print(f"📊 Status: {dados['status']}")
    print()
    print("Próximo passo: enviar o e-mail via GMAIL_SEND_EMAIL com o HTML acima,")
    print("depois rodar:  python3 aprovacao.py marcar %s pendente --message-id <id>" % slug)


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
    dados = carregar(args.slug)
    if not dados:
        raise SystemExit(f"❌ Nenhuma aprovação para '{args.slug}'")
    resumo = {k: v for k, v in dados.items() if k != "legenda"}
    print(json.dumps(resumo, ensure_ascii=False, indent=2))
    print(f"\n--- legenda ({len(dados['legenda'])} caracteres) ---")
    print(dados["legenda"])


def cmd_marcar(args):
    dados = carregar(args.slug)
    if not dados:
        raise SystemExit(f"❌ Nenhuma aprovação para '{args.slug}'")
    if args.status not in STATUS_VALIDOS:
        raise SystemExit(f"❌ Status inválido. Use: {', '.join(STATUS_VALIDOS)}")

    anterior = dados["status"]
    dados["status"] = args.status
    if args.message_id:
        dados["email"]["message_id"] = args.message_id
    if args.thread_id:
        dados["email"]["thread_id"] = args.thread_id
    if args.status == "aprovado":
        dados["aprovado_em"] = agora()
    registrar_evento(dados, "status", f"{anterior} → {args.status} {args.detalhe or ''}".strip())
    salvar(dados)
    print(f"✅ {args.slug}: {anterior} → {args.status}")


def cmd_publicar(args):
    dados = carregar(args.slug)
    if not dados:
        raise SystemExit(f"❌ Nenhuma aprovação para '{args.slug}'")
    if dados["status"] not in ("aprovado", "publicado"):
        raise SystemExit(
            f"❌ Status atual é '{dados['status']}'. Só publica depois de 'aprovado'."
        )
    dados["status"] = "publicado"
    dados["publicacao"] = {
        "media_id": args.media_id,
        "permalink": args.permalink,
        "publicado_em": agora(),
    }
    registrar_evento(dados, "publicado", args.permalink or "")
    salvar(dados)
    print(f"✅ {args.slug} publicado: {args.permalink}")


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
