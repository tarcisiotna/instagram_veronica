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
FONT_BODY = "TT Norms"
BRAND_NAME = "Verônica Bomfim de Lima"
INSTA_HANDLE = "@veronicabomfim.nutri"
CONTACT_PHONE = "(81) 9 9864-5846"
CONTACT_EMAIL = "veronicabomfim.nutri@gmail.com"
SITE = "https://veronicabomfimnutriweb.pages.dev/"
TOTAL_SLIDES = 8

img1_path = escolher_imagem_capa(tema="beneficios-creatina")

IMG_DIR = BASE_DIR / "slides" / "beneficios-creatina" / "imgs"
cta_path = BASE_DIR / "Imagens" / "CTA" / "CTA.png"

def encode_img(path):
    if not path or not path.exists():
        return None
    suffix = path.suffix.lower()
    if suffix in (".jpeg", ".jpg"):
        mime = "image/jpeg"
    elif suffix == ".png":
        mime = "image/png"
    elif suffix == ".webp":
        mime = "image/webp"
    else:
        mime = "image/jpeg"
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"

img1_b64 = encode_img(img1_path)
cta_b64 = encode_img(cta_path)
creatina_b64 = encode_img(IMG_DIR / "creatina.jpg")
academia_b64 = encode_img(IMG_DIR / "academia.jpg")
cerebro_b64 = encode_img(IMG_DIR / "cerebro.jpg")
produto_b64 = encode_img(IMG_DIR / "creatina_produto.webp")

def swipe_arrow(is_light):
    bg = "rgba(0,0,0,0.06)" if is_light else "rgba(255,255,255,0.08)"
    stroke = "rgba(0,0,0,0.25)" if is_light else "rgba(255,255,255,0.35)"
    return f'''<div style="position:absolute;right:0;top:0;bottom:0;width:48px;z-index:9;display:flex;align-items:center;justify-content:center;background:linear-gradient(to right,transparent,{bg});">
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="{stroke}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
</div>'''

slides = []

# ---------- SLIDE 1: CAPA ----------
img1_html = ""
if img1_b64:
    img1_html = f'<img src="{img1_b64}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;"><div style="position:absolute;inset:0;background:linear-gradient(to bottom, rgba(0,0,0,0.35) 0%, rgba(0,0,0,0.7) 100%);z-index:1;"></div>'

slides.append(f'''<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;position:relative;">
  <div style="position:relative;z-index:2;">
    <div style="display:flex;justify-content:center;margin-bottom:20px;">
      <img src="{produto_b64}" style="width:348px;height:auto;object-fit:contain;border-radius:18px;box-shadow:0 14px 40px rgba(0,0,0,0.45);">
    </div>
    <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:14px;background:rgba(57,66,51,0.55);padding:6px 12px;border-radius:20px;">SUPLEMENTAÇÃO E CÉREBRO</span>
    <h1 style="font-family:'{FONT_HEADING}',serif;font-size:32px;font-weight:700;color:#fff;line-height:1.1;margin:0 0 14px 0;">Creatina: muito além dos músculos</h1>
    <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.9);line-height:1.5;margin:0 0 20px 0;">O suplemento mais estudado do mundo também protege a saúde do cérebro.</p>
    <div style="display:flex;align-items:center;gap:12px;margin-top:4px;">
      <div style="width:40px;height:40px;border-radius:50%;background:{BRAND_PRIMARY};display:flex;align-items:center;justify-content:center;color:#fff;font-size:18px;font-weight:700;">V</div>
      <div>
        <span style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;font-weight:600;color:#fff;display:block;letter-spacing:0.5px;">{BRAND_NAME}</span>
        <span style="font-family:'{FONT_BODY}',sans-serif;font-size:11px;color:rgba(255,255,255,0.7);">{INSTA_HANDLE}</span>
      </div>
    </div>
  </div>
  {swipe_arrow(False)}
</div>''')

# ---------- SLIDE 2: O QUE É CREATINA ----------
slides.append(f'''<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;position:relative;">
  <img src="{creatina_b64}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;opacity:0.16;">
  <div style="position:relative;z-index:2;">
    <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:16px;">O QUE É</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 14px 0;">Energia para músculos e cérebro</h2>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.7);line-height:1.5;margin:0 0 16px 0;">A creatina é um composto natural produzido pelo corpo e encontrado na carne e no peixe. Ela aumenta a energia rápida (ATP) das células — e o cérebro é um dos maiores consumidores dessa energia.</p>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:4px;">
    <span style="font-size:11px;padding:5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:{BRAND_LIGHT};">⚡ ATP</span>
    <span style="font-size:11px;padding:5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:{BRAND_LIGHT};">🧠 Neurologia</span>
    <span style="font-size:11px;padding:5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:{BRAND_LIGHT};">💪 Performance</span>
  </div>
  </div>
  {swipe_arrow(False)}
</div>''')

# ---------- SLIDE 3: COGNIÇÃO E CÉREBRO (DESTAQUE) ----------
slides.append(f'''<div class="slide" style="background:linear-gradient(165deg, {BRAND_DARK} 0%, {BRAND_PRIMARY} 50%, {BRAND_LIGHT} 100%);display:flex;flex-direction:column;justify-content:center;padding:0 36px;overflow:hidden;position:relative;">
  <img src="{cerebro_b64}" style="position:absolute;right:-40px;top:-30px;width:200px;height:auto;opacity:0.18;border-radius:16px;object-fit:cover;z-index:0;">
  <div style="position:relative;z-index:2;">
    <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:rgba(255,255,255,0.8);margin-bottom:16px;">DESTAQUE: COGNIÇÃO</span>
    <h2 style="font-family:'{FONT_HEADING}',serif;font-size:30px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 18px 0;">Um cérebro mais ligado</h2>
    <div style="padding:18px;background:rgba(0,0,0,0.25);border-radius:12px;border:1px solid rgba(255,255,255,0.15);margin-bottom:14px;">
      <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:rgba(255,255,255,0.7);margin:0 0 8px 0;">Estudos</p>
      <p style="font-family:'{FONT_HEADING}',serif;font-size:16px;color:#fff;font-style:italic;line-height:1.5;margin:0;">"A suplementação de creatina melhora memória e raciocínio em situações de estresse, privação de sono e fadiga mental."</p>
    </div>
    <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:rgba(255,255,255,0.85);line-height:1.5;margin:0;font-weight:600;">Melhor ainda em quem come pouco peixe e carne (vegetarianos e veganos) 🧠</p>
  </div>
  {swipe_arrow(False)}
</div>''')

# ---------- SLIDE 4: COGNIÇÃO POR FASE DA VIDA ----------
slides.append(f'''<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:16px;">PARA QUEM</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:{DARK_BG};line-height:1.15;margin:0 0 18px 0;">Cérebro protegido em todas as fases</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">👵</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Idosos</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Ajuda a preservar memória e força — aliada contra o declínio</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🎓</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Estudantes</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Mais foco em provas, trabalhos e noites longas de estudo</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">😴</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Quem dorme pouco</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Suaviza o impacto da privação de sono no raciocínio</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🌱</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Vegetarianos e veganos</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Níveis baixos de creatina no cérebro — suplementar compensa</span></div>
    </div>
  </div>
  {swipe_arrow(True)}
</div>''')

# ---------- SLIDE 5: OUTROS BENEFÍCIOS ----------
slides.append(f'''<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;position:relative;">
  <img src="{academia_b64}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;opacity:0.14;">
  <div style="position:relative;z-index:2;">
    <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:16px;">TAMBÉM AJUDA</span>
    <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 18px 0;">E o corpo também agradece</h2>
    <div style="display:flex;flex-direction:column;gap:0;">
      <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.08);">
        <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">💪</span>
        <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Mais força e massa magra</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Um dos suplementos com mais evidência científica</span></div>
      </div>
      <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.08);">
        <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🏋️</span>
        <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Melhor desempenho no treino</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Mais repetições, mais carga, melhor rendimento</span></div>
      </div>
      <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.08);">
        <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🔄</span>
        <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Recuperação acelerada</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Menos fadiga entre séries e entre treinos</span></div>
      </div>
      <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;">
        <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🦴</span>
        <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Fortalecimento ósseo</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);;">Estudos mostram efeito positivo na densidade óssea</span></div>
      </div>
    </div>
  </div>
  {swipe_arrow(False)}
</div>''')

# ---------- SLIDE 6: COMO TOMAR ----------
slides.append(f'''<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:16px;">COMO TOMAR</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:{DARK_BG};line-height:1.15;margin:0 0 18px 0;">Simples e seguro</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">01</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Dose: 3 a 5g por dia</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Creatina monoidratada — a mais estudada</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">02</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Todo dia, em qualquer horário</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Não precisa de "fase de saturação" — constância é o que importa</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">03</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Mantenha-se hidratado</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Beba bastante água ao longo do dia</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">04</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Resultados em 3 a 4 semanas</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Saturação dos músculos e do cérebro leva um tempo</span></div>
    </div>
  </div>
  {swipe_arrow(True)}
</div>''')

# ---------- SLIDE 7: MITOS E VERDADES ----------
slides.append(f'''<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:16px;">MITO OU VERDADE?</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 16px 0;">Desvendando os medos</h2>
  <div style="display:flex;flex-direction:column;gap:10px;margin-bottom:16px;">
    <div style="padding:14px 16px;background:rgba(255,255,255,0.06);border-radius:10px;border:1px solid rgba(255,255,255,0.1);">
      <span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;font-weight:600;color:#94a3b8;display:block;letter-spacing:1px;">MITO</span>
      <span style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:rgba(255,255,255,0.7);">"Creatina estufa a barriga" e "faz mal ao rim" — sem evidência em doses adequadas e pessoas saudáveis</span>
    </div>
    <div style="padding:14px 16px;background:rgba(191,149,102,0.12);border-radius:10px;border:1px solid {BRAND_PRIMARY};">
      <span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;font-weight:600;color:{BRAND_LIGHT};display:block;letter-spacing:1px;">VERDADE</span>
      <span style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:#fff;">É um dos suplementos mais seguros e estudados — a retenção de água é intramuscular, não gordura</span>
    </div>
  </div>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.85);line-height:1.5;margin:0;font-weight:600;">Sempre avalie rins e individualize com um nutricionista 🩺</p>
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
  <title>{BRAND_NAME} - Benefícios da Creatina</title>
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
      <span class="handle">{INSTA_HANDLE}</span> Creatina: muito além dos músculos — ela também cuida do seu cérebro! Descubra os benefícios cognitivos, como tomar e desvende os mitos. 🧠💪 #creatina #suplementacao
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

output_dir = BASE_DIR / "slides" / "beneficios-creatina"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "carousel.html"
output_path.write_text(html, encoding="utf-8")

legenda = f"""{INSTA_HANDLE}

Creatina: muito além dos músculos — o suplemento que também cuida do cérebro

📌 Descrição:
A creatina é um dos suplementos mais estudados do mundo — e a ciência mostra que seus benefícios vão muito além da musculação. Neste carrossel, você vai descobrir como ela melhora memória e raciocínio, especialmente em situações de estresse e privação de sono, além de seus efeitos na força, massa magra e recuperação. Também mostro como tomar, para quem é indicada e quais são os mitos que você deve deixar de acreditar.

📝 Resumo:
• Creatina é energia: aumenta o ATP — o combustível rápido das células, incluindo as do cérebro
• Melhora memória e raciocínio sob estresse, fadiga mental e privação de sono
• Benefícios ainda maiores em vegetarianos e veganos, que têm níveis mais baixos de creatina
• Para o corpo: mais força, massa magra, recuperação e até efeito na densidade óssea
• Dose: 3 a 5g por dia de creatina monoidratada, todo dia, com boa hidratação
• Segura em pessoas saudáveis — o "estufar barriga" é retenção de água intramuscular, não gordura

📚 Fontes:
ISSN — International Society of Sports Nutrition (position stand sobre creatina)
PubMed — estudos clínicos sobre creatina e cognição
Literatura científica revisada sobre suplementação e neurologia

🏷️ Hashtags:
#creatina #suplementacao #cerebro #cognicao #memoria #saudecerebral #nutricao #performance #musculacao #saude #bemestar #nutricionista #veronicabomfim #recife

📞 Contato:
📱 {CONTACT_PHONE}
📧 {CONTACT_EMAIL}
📸 {INSTA_HANDLE}
🌐 {SITE}"""

output_dir.joinpath("legenda.txt").write_text(legenda, encoding="utf-8")

html_size_mb = len(html.encode('utf-8')) / 1024 / 1024
print(f"✅ HTML gerado: {output_path}")
print(f"📦 Tamanho: {html_size_mb:.2f}MB")
print(f"🖼️  Imagem Slide 1: {img1_path.name if img1_path else 'Nenhuma'}")
print(f"📐 Total de slides: {TOTAL_SLIDES}")
print(f"📝 Legenda criada: {output_dir / 'legenda.txt'}")
print("Aviso: As barras de progresso serão adicionadas pelo script de exportação.")
