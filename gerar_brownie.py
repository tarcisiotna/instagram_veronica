import base64
from pathlib import Path

BASE_DIR = Path(__file__).parent

BRAND_PRIMARY = "#bf9566"
BRAND_LIGHT = "#ecd7ba"
BRAND_DARK = "#394233"
LIGHT_BG = "#FAF9F7"
LIGHT_BORDER = "#ecd7ba"
DARK_BG = "#394233"
FONT_HEADING = "Playfair Display"
FONT_BODY = "TT Norms"
BRAND_NAME = "Verônica Bomfim de Lima"
INSTA_HANDLE = "@veronicabomfim.nutri"
CONTACT_PHONE = "(81) 9 9864-5846"
CONTACT_EMAIL = "veronicabomfim.nutri@gmail.com"
SITE = "https://veronicabomfimnutriweb.pages.dev/"
TOTAL_SLIDES = 8

IMG_DIR = BASE_DIR / "slides" / "brownie-fit" / "imgs"
CTA_PATH = BASE_DIR / "Imagens" / "CTA" / "CTA.png"

def encode_img(path):
    if not path or not path.exists():
        return None
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"

brownie_b64 = encode_img(IMG_DIR / "brownie_capa.png")
cta_b64 = encode_img(CTA_PATH)

INGREDIENTES = [
    ("01", "Iogurte natural", "1 copo", "Cremoso e rico em proteínas", "iogurte.jpg", "🥛"),
    ("02", "Ovos", "3 unidades", "Estrutura e maciez", "ovos.jpg", "🥚"),
    ("03", "Cacau em pó", "3 colheres de sopa", "Sabor intenso de chocolate", "cacau.jpg", "🍫"),
    ("04", "Bananas", "2 unidades", "Doçura natural, sem açúcar", "banana.jpg", "🍌"),
    ("05", "Aveia", "2 colheres de sopa", "Fibras que dão saciedade", "aveia.jpg", "🌾"),
    ("06", "Fermento", "1 colher de sopa", "Ajuda o brownie a crescer", "fermento.jpg", "🫧"),
    ("07", "Castanha de caju", "Quebrada, a gosto", "Crocância e gorduras boas", "castanha.jpg", "🥜"),
]

def swipe_arrow(is_light):
    bg = "rgba(0,0,0,0.06)" if is_light else "rgba(255,255,255,0.08)"
    stroke = "rgba(0,0,0,0.25)" if is_light else "rgba(255,255,255,0.35)"
    return f'''<div style="position:absolute;right:0;top:0;bottom:0;width:48px;z-index:9;display:flex;align-items:center;justify-content:center;background:linear-gradient(to right,transparent,{bg});">
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="{stroke}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
</div>'''

slides = []

# ---------- SLIDE 1: CAPA ----------
slides.append(f'''<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;position:relative;">
  <img src="{brownie_b64}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;">
  <div style="position:absolute;inset:0;background:linear-gradient(to bottom, rgba(0,0,0,0.25) 0%, rgba(0,0,0,0.65) 100%);z-index:1;"></div>
  <div style="position:relative;z-index:2;">
    <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:16px;background:rgba(57,66,51,0.55);padding:6px 12px;border-radius:20px;">RECEITA SAUDÁVEL</span>
    <h1 style="font-family:'{FONT_HEADING}',serif;font-size:34px;font-weight:700;color:#fff;line-height:1.1;margin:0 0 12px 0;">Brownie fit de banana</h1>
    <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.9);line-height:1.5;margin:0 0 22px 0;">Sem açúcar, sem farinha branca e com apenas 7 ingredientes. Vem ver!</p>
    <div style="display:flex;align-items:center;gap:12px;margin-top:8px;">
      <div style="width:40px;height:40px;border-radius:50%;background:{BRAND_PRIMARY};display:flex;align-items:center;justify-content:center;color:#fff;font-size:18px;font-weight:700;">V</div>
      <div>
        <span style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;font-weight:600;color:#fff;display:block;letter-spacing:0.5px;">{BRAND_NAME}</span>
        <span style="font-family:'{FONT_BODY}',sans-serif;font-size:11px;color:rgba(255,255,255,0.7);">{INSTA_HANDLE}</span>
      </div>
    </div>
  </div>
  {swipe_arrow(False)}
</div>''')

# ---------- SLIDES 2-3: INGREDIENTES (grade) ----------
def grade_ingredientes(items, inicio, total_itens):
    rows = []
    for num, nome, qtd, nota, imgfile, emoji in items:
        img_b64 = encode_img(IMG_DIR / imgfile)
        rows.append(f'''<div style="display:flex;align-items:center;gap:14px;padding:9px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <div style="width:64px;height:64px;border-radius:14px;overflow:hidden;flex-shrink:0;position:relative;border:2px solid {BRAND_LIGHT};">
        <img src="{img_b64}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;">
        <div style="position:absolute;top:4px;left:4px;width:20px;height:20px;border-radius:50%;background:{BRAND_PRIMARY};display:flex;align-items:center;justify-content:center;font-size:10px;">{emoji}</div>
      </div>
      <div style="flex:1;">
        <span style="font-family:'{FONT_BODY}',sans-serif;font-size:15px;font-weight:600;color:{DARK_BG};display:block;">{nome}</span>
        <span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:{BRAND_PRIMARY};font-weight:600;">{qtd}</span>
      </div>
      <span style="font-family:'{FONT_HEADING}',serif;font-size:18px;font-weight:300;color:{BRAND_PRIMARY};flex-shrink:0;">{num}</span>
    </div>''')
    return "\n".join(rows)

slides.append(f'''<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:16px;">INGREDIENTES</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:{DARK_BG};line-height:1.15;margin:0 0 14px 0;">O que você vai precisar</h2>
  <div style="display:flex;flex-direction:column;">
    {grade_ingredientes(INGREDIENTES[:4], 1, 7)}
  </div>
  <span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;margin-top:12px;text-align:center;">Parte 1 de 2 — role para ver o restante 👉</span>
  {swipe_arrow(True)}
</div>''')

slides.append(f'''<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:16px;">INGREDIENTES</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:{DARK_BG};line-height:1.15;margin:0 0 14px 0;">E só mais 3 ingredientes</h2>
  <div style="display:flex;flex-direction:column;">
    {grade_ingredientes(INGREDIENTES[4:], 5, 7)}
  </div>
  <div style="padding:14px 16px;background:{BRAND_PRIMARY};border-radius:10px;margin-top:14px;">
    <span style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;font-weight:600;color:#fff;">Tudo natural: sem açúcar e sem farinha branca 🍃</span>
  </div>
  {swipe_arrow(True)}
</div>''')

# ---------- SLIDES 4-5: MODO DE PREPARO ----------
slides.append(f'''<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:16px;">MODO DE PREPARO</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 18px 0;">Primeiro, bata os ingredientes</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;border-bottom:1px solid rgba(255,255,255,0.08);">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">01</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Bata todos os ingredientes no liquidificador</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Reserve a castanha e o fermento</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">02</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Depois de bater tudo, acrescente a castanha e o fermento</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Misture delicadamente até incorporar</span></div>
    </div>
  </div>
  {swipe_arrow(False)}
</div>''')

slides.append(f'''<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:16px;">MODO DE PREPARO</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:{DARK_BG};line-height:1.15;margin:0 0 18px 0;">Depois, é só assar</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">03</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Coloque em uma forma untada</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Espalhe a massa de forma uniforme</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">04</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Leve ao forno a 180°C por 30 minutos</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Espere esfriar para cortar — fica mais firme!</span></div>
    </div>
  </div>
  <div style="padding:14px 16px;background:{BRAND_PRIMARY};border-radius:10px;margin-top:16px;">
    <span style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;font-weight:600;color:#fff;">Dica: faça o teste do palito — saia limpo, está pronto 🍫</span>
  </div>
  {swipe_arrow(True)}
</div>''')

# ---------- SLIDE 6: POR QUE É FIT ----------
slides.append(f'''<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:16px;">POR QUE É FIT?</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 18px 0;">Sabor de sobremesa, coração leve</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.08);">
      <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🍬</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Sem açúcar refinado</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Doçura vem da banana madura</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.08);">
      <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🌾</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Sem farinha branca</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">A aveia entra no lugar, com fibras</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.08);">
      <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🥛</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Proteínas e gorduras boas</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Iogurte, ovos e castanha de caju</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;">
      <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">⏱️</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Pronto em 40 minutos</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">10 min de preparo + 30 min no forno</span></div>
    </div>
  </div>
  {swipe_arrow(False)}
</div>''')

# ---------- SLIDE 7: CONVITE ----------
slides.append(f'''<div class="slide" style="background:linear-gradient(165deg, {BRAND_DARK} 0%, {BRAND_PRIMARY} 50%, {BRAND_LIGHT} 100%);display:flex;flex-direction:column;justify-content:center;padding:0 36px;overflow:hidden;text-align:center;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:rgba(255,255,255,0.8);margin-bottom:18px;">VAMOS TESTAR?</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:32px;font-weight:700;color:#fff;line-height:1.15;margin:0 0 18px 0;">Salva para não perder! 🔖</h2>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.9);line-height:1.6;margin:0 0 24px 0;">Marque alguém que precisa dessa sobremesa saudável e me conta nos comentários se você vai fazer em casa. 🍫</p>
  <div style="padding:18px;background:rgba(0,0,0,0.25);border-radius:12px;border:1px solid rgba(255,255,255,0.15);">
    <p style="font-family:'{FONT_HEADING}',serif;font-size:17px;color:#fff;font-style:italic;line-height:1.5;margin:0;">"Comer saudável não precisa ser sem graça — dá para ser fit e delicioso."</p>
  </div>
  {swipe_arrow(False)}
</div>''')

# ---------- SLIDE 8: CTA ----------
slides.append(f'''<div class="slide" style="display:flex;flex-direction:column;justify-content:center;align-items:center;padding:0;overflow:hidden;position:relative;">
  <img src="{cta_b64}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;">
  <div style="position:absolute;bottom:0;left:0;right:0;padding:30px 20px;background:linear-gradient(to top,rgba(57,66,51,0.95),rgba(57,66,51,0.7),transparent);text-align:center;">
  </div>
</div>''')

slides_html = "\n".join(slides)
dots_html = "\n".join(f'<div class="dot{" active" if i==0 else ""}" data-index="{i}"></div>' for i in range(TOTAL_SLIDES))

html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=420">
  <title>{BRAND_NAME} - Brownie Fit</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: '{FONT_BODY}', sans-serif; background: #0F1A0F; padding: 20px; display: flex; justify-content: center; }}
    .ig-frame {{ width: 420px; max-width: 100%; border-radius: 12px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.5); background: #000; }}
    .ig-header {{ display: flex; align-items: center; gap: 10px; padding: 12px 16px; background: {DARK_BG}; color: #fff; }}
    .ig-header .avatar {{ width: 32px; height: 32px; border-radius: 50%; background: {BRAND_PRIMARY}; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 14px; font-weight: 700; flex-shrink: 0; }}
    .ig-header .handle {{ font-size: 13px; font-weight: 600; }}
    .ig-header .subtitle {{ font-size: 11px; color: rgba(255,255,255,0.5); margin-left: auto; }}
    .carousel-viewport {{ width: 420px; height: 525px; overflow: hidden; cursor: grab; position: relative; touch-action: pan-y; user-select: none; }}
    .carousel-track {{ display: flex; transition: transform 0.3s ease; will-change: transform; }}
    .slide {{ position:relative; width:420px; height:525px; flex-shrink: 0; }}
    .serif {{ font-family: '{FONT_HEADING}', serif; }}
    .sans {{ font-family: '{FONT_BODY}', sans-serif; }}
  </style>
</head>
<body>
  <div class="ig-frame">
    <div class="ig-header">
      <div class="avatar">V</div>
      <span class="handle">{INSTA_HANDLE}</span>
      <span class="subtitle">Nutrição</span>
    </div>
    <div class="carousel-viewport" id="viewport">
      <div class="carousel-track" id="track">
        {slides_html}
      </div>
    </div>
    <div class="ig-dots" id="dots">
      {dots_html}
    </div>
    <div class="ig-actions">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-left:auto;"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
    </div>
    <div class="ig-caption">
      <span class="handle">{INSTA_HANDLE}</span> Brownie fit de banana com apenas 7 ingredientes! 🍫 Bata tudo, acrescente a castanha e o fermento, e leve ao forno a 180°C por 30 minutos. Salve para testar! 🍌 #browniefit #receitasaudavel
      <span class="time">2 HOURS AGO</span>
    </div>
  </div>
  <script>
    const viewport = document.getElementById('viewport');
    const track = document.getElementById('track');
    const dots = document.querySelectorAll('.dot');
    let current = 0;
    let startX = 0;
    let isDragging = false;
    function goTo(idx) {{
      current = Math.max(0, Math.min(idx, {TOTAL_SLIDES - 1}));
      track.style.transform = 'translateX(' + (-current * 420) + 'px)';
      dots.forEach((d, i) => d.classList.toggle('active', i === current));
    }}
    viewport.addEventListener('pointerdown', e => {{ startX = e.clientX; isDragging = true; viewport.style.cursor = 'grabbing'; }});
    viewport.addEventListener('pointermove', e => {{ if (!isDragging) return; e.preventDefault(); }});
    viewport.addEventListener('pointerup', e => {{
      if (!isDragging) return;
      isDragging = false; viewport.style.cursor = 'grab';
      const diff = startX - e.clientX;
      if (Math.abs(diff) > 50) {{ diff > 0 ? goTo(current + 1) : goTo(current - 1); }}
    }});
    viewport.addEventListener('click', () => {{ if (!isDragging) goTo(current + 1); }});
  </script>
</body>
</html>
'''

output_dir = BASE_DIR / "slides" / "brownie-fit"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "carousel.html"
output_path.write_text(html, encoding="utf-8")

legenda = f"""{INSTA_HANDLE}

Brownie fit de banana: a sobremesa saudável com apenas 7 ingredientes

📌 Descrição:
Quer um brownie delicioso sem açúcar e sem farinha branca? Essa receita leva apenas 7 ingredientes: iogurte natural, ovos, cacau em pó, banana, aveia, fermento e castanha de caju. As bananas dão a doçura natural, o cacau garante o sabor intenso de chocolate e a aveia adiciona fibras e saciedade. Perfeito para o lanche da tarde sem sair da alimentação equilibrada.

📝 Resumo:
• 1 copo de iogurte natural — cremosidade e proteínas
• 3 ovos — estrutura e maciez
• 3 colheres de sopa de cacau em pó — sabor intenso de chocolate
• 2 bananas maduras — doçura natural, sem açúcar
• 2 colheres de sopa de aveia — fibras e saciedade
• 1 colher de sopa de fermento — ajuda a crescer
• Castanha de caju quebrada a gosto — crocância e gorduras boas

Modo de preparo:
• Bata todos os ingredientes no liquidificador, reservando a castanha e o fermento
• Depois de bater tudo, acrescente a castanha e o fermento e misture delicadamente
• Coloque em uma forma untada
• Leve ao forno a 180°C por 30 minutos — faça o teste do palito

📚 Fontes:
Receita prática elaborada pela nutricionista — nutrientes avaliados a partir da tabela de composição de alimentos (TACO/IBGE).

🏷️ Hashtags:
#browniefit #receitasaudavel #browniedebanana #sobremesasfit #nutricao #alimentacaosaudavel #receitascomcacau #lanchesaudavel #fit #saude #veronicabomfim #recife

📞 Contato:
📱 {CONTACT_PHONE}
📧 {CONTACT_EMAIL}
📸 {INSTA_HANDLE}
🌐 {SITE}"""

output_dir.joinpath("legenda.txt").write_text(legenda, encoding="utf-8")

html_size_mb = len(html.encode('utf-8')) / 1024 / 1024
print(f"✅ HTML gerado: {output_path}")
print(f"📦 Tamanho: {html_size_mb:.2f}MB")
print(f"📐 Total de slides: {TOTAL_SLIDES}")
print(f"📝 Legenda criada: {output_dir / 'legenda.txt'}")
print("Aviso: As barras de progresso serão adicionadas pelo script de exportação.")
