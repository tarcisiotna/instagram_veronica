import base64
from pathlib import Path

from imagem_capa import escolher_imagem_capa

BASE_DIR = Path(__file__).parent

BRAND_PRIMARY = "#bf9566"
BRAND_LIGHT = "#ecd7ba"
BRAND_DARK = "#394233"
LIGHT_BG = "#FAF9F7"
LIGHT_BORDER = "#ecd7ba"
DARK_BG = "#394233"
FONT_HEADING = "Playfair Display"
FONT_BODY = "Inter"
BRAND_NAME = "Verônica Bomfim de Lima"
INSTA_HANDLE = "@veronicabomfim.nutri"
TEMA = "perda-peso-onco"
TOTAL_SLIDES = 8

img1_path = escolher_imagem_capa(tema=TEMA)

cta_path = BASE_DIR / "Imagens" / "CTA" / "CTA.png"


def encode_img(path):
    if not path or not path.exists():
        return None
    mime = "image/jpeg" if path.suffix.lower() in (".jpeg", ".jpg") else "image/png"
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"


img1_b64 = encode_img(img1_path)
cta_b64 = encode_img(cta_path)


def swipe_arrow(is_light):
    bg = "rgba(0,0,0,0.06)" if is_light else "rgba(255,255,255,0.08)"
    stroke = "rgba(0,0,0,0.25)" if is_light else "rgba(255,255,255,0.35)"
    return f'''<div style="position:absolute;right:0;top:0;bottom:0;width:48px;z-index:9;display:flex;align-items:center;justify-content:center;background:linear-gradient(to right,transparent,{bg});">
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="{stroke}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
</div>'''


slides = []

# ---------------------------------------------------------------- slide 1
img1_html = ""
if img1_b64:
    img1_html = (
        f'<img src="{img1_b64}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;">'
        '<div style="position:absolute;inset:0;background:linear-gradient(to bottom, rgba(0,0,0,0.25) 0%, rgba(0,0,0,0.82) 100%);z-index:1;"></div>'
    )

slides.append(f'''<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:center;padding:0 36px;overflow:hidden;position:relative;">
  {img1_html}
  <div style="position:relative;z-index:2;">
    <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:16px;">PERDA DE PESO</span>
    <h1 style="font-family:'{FONT_HEADING}',serif;font-size:29px;font-weight:700;color:#fff;line-height:1.12;margin:0 0 16px 0;">Emagreceu sem querer durante o tratamento?</h1>
    <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13.5px;color:rgba(255,255,255,0.9);line-height:1.55;margin:0 0 26px 0;">Quando a perda de peso deixa de ser conquista e passa a ser sinal de alerta.</p>
    <div style="display:flex;align-items:center;gap:12px;margin-top:4px;">
      <div style="width:40px;height:40px;border-radius:50%;background:{BRAND_PRIMARY};display:flex;align-items:center;justify-content:center;color:#fff;font-size:18px;font-weight:700;">V</div>
      <div>
        <span style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;font-weight:600;color:#fff;display:block;letter-spacing:0.3px;">{BRAND_NAME}</span>
        <span style="font-family:'{FONT_BODY}',sans-serif;font-size:11px;color:rgba(255,255,255,0.7);;">{INSTA_HANDLE}</span>
      </div>
    </div>
  </div>
  {swipe_arrow(False)}
</div>''')

# ---------------------------------------------------------------- slide 2
slides.append(f'''<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:16px;">ATENÇÃO</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:27px;font-weight:600;color:{DARK_BG};line-height:1.15;margin:0 0 14px 0;">Nem toda perda de peso é boa notícia</h2>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13.5px;color:#5C5A55;line-height:1.6;margin:0 0 20px 0;">Durante o tratamento oncológico, o corpo pode perder <strong style="color:{DARK_BG};">músculo antes de perder gordura</strong>. Na balança o número cai — mas a força, a imunidade e a resposta ao tratamento caem junto.</p>
  <div style="display:flex;gap:8px;flex-wrap:wrap;">
    <span style="font-size:11px;padding:5px 12px;border:1px solid {LIGHT_BORDER};border-radius:20px;color:#A8A29A;text-decoration:line-through;">Emagrecer é sempre positivo</span>
    <span style="font-size:11px;padding:5px 12px;border:1px solid {LIGHT_BORDER};border-radius:20px;color:#A8A29A;text-decoration:line-through;">É só efeito do tratamento</span>
    <span style="font-size:11px;padding:5px 12px;border:1px solid {LIGHT_BORDER};border-radius:20px;color:#A8A29A;text-decoration:line-through;">Depois eu recupero</span>
  </div>
  {swipe_arrow(True)}
</div>''')

# ---------------------------------------------------------------- slide 3
slides.append(f'''<div class="slide" style="background:linear-gradient(165deg, {BRAND_DARK} 0%, #4A5540 45%, {BRAND_PRIMARY} 100%);display:flex;flex-direction:column;justify-content:center;padding:0 36px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:rgba(255,255,255,0.8);margin-bottom:16px;">ENTENDA</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 16px 0;">Quando a perda de peso tem nome: caquexia</h2>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:rgba(255,255,255,0.85);line-height:1.6;margin:0 0 18px 0;">É uma síndrome metabólica com perda involuntária de peso e de massa muscular, acompanhada de inflamação. Não se resolve apenas comendo mais.</p>
  <div style="padding:18px 20px;background:rgba(0,0,0,0.28);border-radius:12px;border:1px solid rgba(255,255,255,0.15);margin-bottom:14px;">
    <p style="font-family:'{FONT_HEADING}',serif;font-size:30px;font-weight:700;color:{BRAND_LIGHT};line-height:1;margin:0 0 6px 0;">~50%</p>
    <p style="font-family:'{FONT_BODY}',sans-serif;font-size:12.5px;color:rgba(255,255,255,0.85);line-height:1.5;margin:0;">dos pacientes com câncer apresentam caquexia. Nos casos avançados, passa de dois terços.</p>
  </div>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:10.5px;color:rgba(255,255,255,0.6);line-height:1.5;margin:0;">Fontes: Consenso Brasileiro de Caquexia (2011) · ESPEN · INCA</p>
  {swipe_arrow(False)}
</div>''')

# ---------------------------------------------------------------- slide 4
sinais = [
    ("01", "Perda de mais de 5% do peso em 6 meses", "Sem dieta e sem intenção"),
    ("02", "Roupas ficando largas sem motivo", "O espelho demora a mostrar, a roupa não"),
    ("03", "Fraqueza em tarefas simples", "Subir escada, abrir um pote, carregar compras"),
    ("04", "Saciedade precoce", "Come pouco e já se sente cheio"),
    ("05", "Perda visível de massa muscular", "Braços e pernas afinando rápido"),
]
sinais_html = "\n".join(
    f'''    <div style="display:flex;align-items:flex-start;gap:14px;padding:9px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:20px;font-weight:400;color:{BRAND_PRIMARY};min-width:26px;line-height:1.1;flex-shrink:0;">{n}</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;font-weight:600;color:{DARK_BG};display:block;line-height:1.35;">{t}</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:11px;color:#8A8580;line-height:1.4;">{d}</span></div>
    </div>''' for n, t, d in sinais
)

slides.append(f'''<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 58px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:12px;">SINAIS DE ALERTA</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:600;color:{DARK_BG};line-height:1.15;margin:0 0 12px 0;">5 sinais para levar a sério</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
{sinais_html}
  </div>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:10.5px;color:#8A8580;line-height:1.5;margin:12px 0 0 0;">Perda acima de 2% com IMC abaixo de 20 também é critério de alerta.</p>
  {swipe_arrow(True)}
</div>''')

# ---------------------------------------------------------------- slide 5
consequencias = [
    ("Menos tolerância à quimioterapia", "Pode levar à redução de dose e atraso no ciclo"),
    ("Mais infecções", "A imunidade cai junto com a massa muscular"),
    ("Mais fadiga", "Menos disposição para o dia a dia e para o tratamento"),
    ("Pior recuperação cirúrgica", "Mais tempo de internação e de cicatrização"),
]
cons_html = "\n".join(
    f'''    <div style="display:flex;align-items:flex-start;gap:14px;padding:11px 0;border-bottom:1px solid rgba(255,255,255,0.1);">
      <span style="color:{BRAND_LIGHT};font-size:14px;width:16px;text-align:center;flex-shrink:0;">✦</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;font-weight:600;color:#fff;display:block;">{t}</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:11.5px;color:rgba(255,255,255,0.6);">{d}</span></div>
    </div>''' for t, d in consequencias
)

slides.append(f'''<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 50px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:14px;">POR QUE IMPORTA</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 14px 0;">O que a perda de peso rouba do tratamento</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
{cons_html}
  </div>
  {swipe_arrow(False)}
</div>''')

# ---------------------------------------------------------------- slide 6
passos = [
    ("01", "Pese-se 1x por semana", "Mesmo dia, mesmo horário, mesma balança. Anote o valor."),
    ("02", "Não espere o tratamento acabar", "Procure um nutricionista oncológico ao notar a perda de peso."),
    ("03", "Ajuste com acompanhamento", "Proteína, energia e suplementação oral só com indicação profissional."),
]
passos_html = "\n".join(
    f'''    <div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:25px;font-weight:300;color:{BRAND_PRIMARY};min-width:32px;line-height:1;flex-shrink:0;">{n}</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:13.5px;font-weight:600;color:{DARK_BG};display:block;line-height:1.35;">{t}</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:11.5px;color:#8A8580;line-height:1.45;">{d}</span></div>
    </div>''' for n, t, d in passos
)

slides.append(f'''<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 50px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:14px;">O QUE FAZER</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:600;color:{DARK_BG};line-height:1.15;margin:0 0 16px 0;">3 passos se você notou perda de peso</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
{passos_html}
  </div>
  {swipe_arrow(True)}
</div>''')

# ---------------------------------------------------------------- slide 7
slides.append(f'''<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:center;padding:0 36px;overflow:hidden;position:relative;">
  <div style="position:absolute;top:-60px;right:-60px;width:220px;height:220px;border-radius:50%;background:radial-gradient(circle,rgba(191,149,102,0.22) 0%,transparent 70%);"></div>
  <div style="position:relative;z-index:2;">
    <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:18px;">LEMBRE-SE</span>
    <h2 style="font-family:'{FONT_HEADING}',serif;font-size:31px;font-weight:600;color:#fff;line-height:1.2;margin:0 0 18px 0;">Perder peso não é meta.<br><span style="color:{BRAND_LIGHT};">Manter força é.</span></h2>
    <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:rgba(255,255,255,0.7);line-height:1.6;margin:0 0 24px 0;">Se você ou alguém em tratamento emagreceu sem querer, isso merece avaliação — não comemoração.</p>
    <div style="display:inline-flex;align-items:center;gap:10px;padding:10px 16px;border:1px solid rgba(255,255,255,0.18);border-radius:24px;">
      <span style="font-size:13px;">💾</span>
      <span style="font-family:'{FONT_BODY}',sans-serif;font-size:11.5px;color:rgba(255,255,255,0.85);">Salve e compartilhe com quem está em tratamento</span>
    </div>
  </div>
  {swipe_arrow(False)}
</div>''')

# ---------------------------------------------------------------- slide 8 (CTA)
slides.append(f'''<div class="slide" style="display:flex;flex-direction:column;justify-content:center;align-items:center;padding:0;overflow:hidden;position:relative;">
  <img src="{cta_b64}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;">
  <div style="position:absolute;bottom:0;left:0;right:0;padding:30px 20px;background:linear-gradient(to top,rgba(57,66,51,0.95),rgba(57,66,51,0.7),transparent);text-align:center;">
  </div>
</div>''')

slides_html = "\n".join(slides)

dots_html = "\n".join(
    f'<div class="dot{" active" if i == 0 else ""}" data-index="{i}"></div>'
    for i in range(TOTAL_SLIDES)
)

html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=420">
  <title>{BRAND_NAME} - Carrossel Instagram</title>
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
      <span class="handle">{INSTA_HANDLE}</span> Emagreceu sem querer durante o tratamento? Nem toda perda de peso é boa notícia. Descubra os sinais de alerta e o que fazer. 🎗️
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

output_dir = BASE_DIR / "slides" / TEMA
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "carousel.html"
output_path.write_text(html, encoding="utf-8")

html_size_mb = len(html.encode("utf-8")) / 1024 / 1024
print(f"✅ HTML gerado: {output_path}")
print(f"📦 Tamanho: {html_size_mb:.2f}MB")
print(f"🖼️  Imagem Slide 1: {img1_path.name if img1_path else 'Nenhuma'}")
print(f"📐 Total de slides: {TOTAL_SLIDES}")
print("\nAviso: as barras de progresso serão adicionadas pelo script de exportação.")
