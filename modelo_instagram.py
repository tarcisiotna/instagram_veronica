import base64
import random
from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent

# ============================================
# VALIDAÇÃO DAS REGRAS - NÃO VIOLAR!
# ============================================
for img_path in [
    str(BASE_DIR / "Imagens" / "foto1.jpeg"),
]:
    if Path(img_path).exists():
        size_mb = Path(img_path).stat().st_size / 1024 / 1024
        if size_mb < 1:
            print(f"⚠️  REGRA VIOLADA: {img_path} tem apenas {size_mb:.1f}MB!")
            print("   Use apenas imagens >7MB: 0AVA3114.jpg, 0AVA3115.jpg, etc.")
            sys.exit(1)

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
TOTAL_SLIDES = 8
CONTACT_PHONE = "(81) 9 9864-5846"
CONTACT_EMAIL = "veronicabomfim.nutri@gmail.com"

PROFILE_IMAGES = [
    str(BASE_DIR / "Imagens" / "nanobanana" / "936f4681-434d-4d17-af25-6ccc34f8846a.jpeg"),
    str(BASE_DIR / "Imagens" / "nanobanana" / "08f51a8e-19df-415e-bbd0-d8e61192c9a7.jpeg"),
    str(BASE_DIR / "Imagens" / "nanobanana" / "2f8f305b-55fa-42c6-ab75-2b258509ad9c.jpeg"),
    str(BASE_DIR / "Imagens" / "nanobanana" / "7f6b31cf-bc56-42d5-9430-afc78d9b4534.jpeg"),
    str(BASE_DIR / "Imagens" / "nanobanana" / "5caa0b8c-9fca-4b7d-8b58-fda5fa092f85.jpeg"),
    str(BASE_DIR / "Imagens" / "nanobanana" / "5e3dd5f4-661b-4329-8496-92dc809e5c73.jpeg"),
    str(BASE_DIR / "Imagens" / "nanobanana" / "5f649b35-80b6-48a1-9d3f-cea879b5f42d.jpeg"),
]

def load_image_base64(image_path):
    path = Path(image_path)
    if not path.exists():
        return None
    mime = "image/jpeg"
    if path.suffix.lower() == ".png":
        mime = "image/png"
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"

slide_images = []
for img_path in PROFILE_IMAGES[:7]:
    img_data = load_image_base64(img_path)
    if img_data:
        slide_images.append(img_data)

profile_data_uri = random.choice(slide_images) if slide_images else None

LOGO_IMAGES = [
    str(BASE_DIR / "Imagens" / "Sem fundo" / "1.png"),
    str(BASE_DIR / "Imagens" / "Sem fundo" / "2.png"),
    str(BASE_DIR / "Imagens" / "Sem fundo" / "3.png"),
    str(BASE_DIR / "Imagens" / "Sem fundo" / "4.png"),
    str(BASE_DIR / "Imagens" / "Sem fundo" / "5.png"),
    str(BASE_DIR / "Imagens" / "Sem fundo" / "6.png"),
    str(BASE_DIR / "Imagens" / "Sem fundo" / "7.png"),
    str(BASE_DIR / "Imagens" / "Sem fundo" / "8.png"),
    str(BASE_DIR / "Imagens" / "Sem fundo" / "9.png"),
]
logo_data_uri = load_image_base64(LOGO_IMAGES[0])

def progress_bar(index, total, is_light):
    pct = ((index + 1) / total) * 100
    track = "rgba(0,0,0,0.08)" if is_light else "rgba(255,255,255,0.12)"
    fill = BRAND_PRIMARY if is_light else "#fff"
    label = "rgba(0,0,0,0.3)" if is_light else "rgba(255,255,255,0.4)"
    return f'''<div style="position:absolute;bottom:0;left:0;right:0;padding:16px 28px 20px;z-index:10;display:flex;align-items:center;gap:10px;">
  <div style="flex:1;height:3px;background:{track};border-radius:2px;overflow:hidden;">
    <div style="height:100%;width:{pct}%;background:{fill};border-radius:2px;"></div>
  </div>
  <span style="font-size:11px;color:{label};font-weight:500;">{index+1}/{total}</span>
</div>'''

def swipe_arrow(is_light):
    if is_light:
        bg = "rgba(0,0,0,0.06)"
        stroke = "rgba(0,0,0,0.25)"
    else:
        bg = "rgba(255,255,255,0.08)"
        stroke = "rgba(255,255,255,0.35)"
    return f'''<div style="position:absolute;right:0;top:0;bottom:0;width:48px;z-index:9;display:flex;align-items:center;justify-content:center;background:linear-gradient(to right,transparent,{bg});">
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
    <path d="M9 6l6 6-6 6" stroke="{stroke}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
</div>'''

topic = sys.argv[1] if len(sys.argv) > 1 else "Mitos e verdades - Nutrição Oncológica"
hook = sys.argv[2] if len(sys.argv) > 2 else "O que realmente funciona na alimentação durante o tratamento"

slide1_img = ""
if profile_data_uri:
    slide1_img = f'''<img src="{profile_data_uri}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;">
  <div style="position:absolute;inset:0;background:linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.6) 100%);z-index:1;"></div>'''

slides = []

slides.append(f'''
<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:center;padding:0 36px;overflow:hidden;position:relative;">
  {slide1_img}
  <div style="position:relative;z-index:2;">
    <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:#fff;margin-bottom:16px;">MITOS E VERDADES</span>
    <h1 style="font-family:'{FONT_HEADING}',serif;font-size:32px;font-weight:700;color:#fff;line-height:1.1;margin:0 0 16px 0;">{hook}</h1>
    <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.9);line-height:1.5;margin:0 0 24px 0;">Nutrição baseada em evidências para pacientes oncológicos</p>
    <div style="display:flex;align-items:center;gap:12px;margin-top:8px;">
      <div style="width:40px;height:40px;border-radius:50%;background:{BRAND_PRIMARY};display:flex;align-items:center;justify-content:center;color:#fff;font-size:18px;font-weight:700;">V</div>
      <div>
        <span style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;font-weight:600;color:#fff;display:block;letter-spacing:0.5px;">{BRAND_NAME}</span>
        <span style="font-family:'{FONT_BODY}',sans-serif;font-size:11px;color:rgba(255,255,255,0.7);">{INSTA_HANDLE}</span>
      </div>
    </div>
  </div>
  {swipe_arrow(False)}
</div>
''')

slides.append(f'''
<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:16px;">MITOS POPULARES</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 14px 0;">Você já ouviu falar que...</h2>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.6);line-height:1.5;margin:0 0 12px 0;">Pacientes vivem cercados de informações erradas sobre alimentação e câncer.</p>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px;">
    <span style="font-size:11px;padding:5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:#94a3b8;text-decoration:line-through;">Açúcar alimenta o câncer</span>
    <span style="font-size:11px;padding:5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:#94a3b8;text-decoration:line-through;">Dieta cetogênica cura câncer</span>
    <span style="font-size:11px;padding:5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:#94a3b8;text-decoration:line-through;">Jejuar potencializa a quimio</span>
  </div>
  {swipe_arrow(False)}
</div>
''')

slides.append(f'''
<div class="slide" style="background:linear-gradient(165deg, {BRAND_DARK} 0%, {BRAND_PRIMARY} 50%, {BRAND_LIGHT} 100%);display:flex;flex-direction:column;justify-content:center;padding:0 36px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:rgba(255,255,255,0.8);margin-bottom:16px;">A VERDADE</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:30px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 20px 0;">A ciência mostra outra coisa</h2>
  <div style="padding:20px;background:rgba(0,0,0,0.25);border-radius:12px;border:1px solid rgba(255,255,255,0.15);margin-bottom:16px;">
    <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:rgba(255,255,255,0.7);margin:0 0 8px 0;">Dica</p>
    <p style="font-family:'{FONT_HEADING}',serif;font-size:16px;color:#fff;font-style:italic;line-height:1.5;margin:0;">"Nenhum alimento sozinho cura ou causa câncer. Toda célula do corpo usa glicose — cortar açúcar não 'mata' o tumor, mas pode desnutrir o paciente."</p>
  </div>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:rgba(255,255,255,0.8);line-height:1.5;margin:0;font-weight:600;">Evidências: INCA, OMS, ESPEN, SBNO.</p>
  {swipe_arrow(False)}
</div>
''')

slides.append(f'''
<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:16px;">O QUE FUNCIONA</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#1e293b;line-height:1.15;margin:0 0 18px 0;">Benefícios comprovados</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">✦</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#1e293b;display:block;">Manter peso e força</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Nutrição adequada preserva massa magra</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">✦</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#1e293b;display:block;">Melhor tolerância ao tratamento</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Menos interrupções por efeitos colaterais</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">✦</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#1e293b;display:block;">Menos efeitos colaterais</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Náuseas, fadiga e mucosite reduzidos</span></div>
    </div>
  </div>
  {swipe_arrow(True)}
</div>
''')

slides.append(f'''
<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:16px;">PRINCÍPIOS</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 14px 0;">O que realmente importa</h2>
  <div style="display:flex;flex-direction:column;gap:10px;">
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.08);">
      <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🥗</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Dieta variada e colorida</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Frutas, legumes, verduras, cereais integrais</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.08);">
      <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🥩</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Proteínas em todas as refeições</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Carnes, ovos, leguminosas, laticínios</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;">
      <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">⚠️</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Nada de suplementos por conta própria</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Podem interferir no tratamento</span></div>
    </div>
  </div>
  {swipe_arrow(False)}
</div>
''')

slides.append(f'''
<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:16px;">PASSO A PASSO</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#1e293b;line-height:1.15;margin:0 0 18px 0;">3 passos para uma nutrição segura</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">01</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#1e293b;display:block;">Avaliação individualizada</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Histórico clínico e estado nutricional</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">02</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#1e293b;display:block;">Plano sem restrições desnecessárias</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Comer bem sem radicalismos</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">03</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#1e293b;display:block;">Suplementação só quando indicada</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Baseada em exames e evidências</span></div>
    </div>
  </div>
  {swipe_arrow(True)}
</div>
''')

cta_img_path = str(BASE_DIR / "Imagens" / "CTA" / "CTA.png")
cta_img_data_uri = None
if Path(cta_img_path).exists():
    b64 = base64.b64encode(Path(cta_img_path).read_bytes()).decode()
    cta_img_data_uri = f"data:image/png;base64,{b64}"
    print(f"✅ CTA image loaded: {len(b64)} chars")
else:
    print("⚠️  CTA.png not found, using fallback gradient")

logo_img_tag = f'<img src="{logo_data_uri}" style="width:180px;height:auto;margin:0 auto 20px;filter:drop-shadow(0 8px 25px rgba(191,149,102,0.6));">' if logo_data_uri else f'<div style="width:100px;height:100px;border-radius:50%;background:{BRAND_PRIMARY};display:flex;align-items:center;justify-content:center;color:#fff;font-size:42px;font-weight:700;margin:0 auto 20px;box-shadow:0 8px 30px rgba(191,149,102,0.6);border:4px solid rgba(255,255,255,0.4);">V</div>'

slides.append(f'''
<div class="slide" style="display:flex;flex-direction:column;justify-content:center;align-items:center;padding:0;overflow:hidden;position:relative;">
  <img src="{cta_img_data_uri}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;">

  <div style="position:absolute;bottom:0;left:0;right:0;padding:30px 20px;background:linear-gradient(to top,rgba(57,66,51,0.95),rgba(57,66,51,0.7),transparent);text-align:center;">
  </div>
</div>
''')

slides_html = "\n".join(slides)
dots_html = "\n".join(f'<div class="dot{" active" if i==0 else ""}" data-index="{i}"></div>' for i in range(TOTAL_SLIDES))

html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{BRAND_NAME} - Carrossel Instagram</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Lora:wght@300;400;600;700&family=Nunito+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
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
    .ig-dots {{ display: flex; justify-content: center; gap: 6px; padding: 10px; background: {DARK_BG}; }}
    .ig-dots .dot {{ width: 6px; height: 6px; border-radius: 50%; background: rgba(255,255,255,0.2); transition: background 0.2s; }}
    .ig-dots .dot.active {{ background: #fff; }}
    .ig-actions {{ display: flex; align-items: center; gap: 16px; padding: 12px 16px; background: {DARK_BG}; color: #fff; }}
    .ig-actions svg {{ width: 24px; height: 24px; }}
    .ig-caption {{ padding: 8px 16px 16px; background: {DARK_BG}; color: #fff; font-size: 13px; }}
    .ig-caption .handle {{ font-weight: 600; }}
    .ig-caption .time {{ color: rgba(255,255,255,0.4); font-size: 11px; margin-left: 8px; }}
    .slide {{ position:relative; width:420px; height:525px; flex-shrink: 0; }}
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
      <span class="handle">{INSTA_HANDLE}</span> {hook} 🥗 Mitos e verdades da nutrição oncológica! #nutrição #câncer #mitoseverdades #oncologia #saúde #veronicabomfim
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

output_file = str(BASE_DIR / "slides" / "mitos-verdades-nutricao-oncologica" / "carousel.html")
Path(output_file).write_text(html, encoding="utf-8")

slides_dir = Path(output_file).parent
slides_dir.mkdir(exist_ok=True)

legenda = f"""{INSTA_HANDLE}

{hook}

📌 Descrição:
[Adicione descrição sobre mitos e verdades da nutrição oncológica]

📝 Resumo:
• [Ponto 1 relevante sobre mitos e verdades]
• [Ponto 2 relevante sobre mitos e verdades]
• [Ponto 3 relevante sobre mitos e verdades]
• [Ponto 4 relevante sobre mitos e verdades]

📚 Fontes:
INCA — Instituto Nacional de Câncer
OMS — Organização Mundial da Saúde
ESPEN — Diretrizes Europeias de Nutrição Clínica
SBNO — Sociedade Brasileira de Nutrição Oncológica

🏷️ Hashtags:
#nutricao #oncologia #mitoseverdades #cancer #tratamentooncologico #nutricionista #veronicabomfim #recife #saude #alimentacao

📞 Contato:
📱 {CONTACT_PHONE}
📧 {CONTACT_EMAIL}
📸 {INSTA_HANDLE}"""

slides_dir.joinpath("legenda.txt").write_text(legenda, encoding="utf-8")

print(f"Carrossel criado: {output_file}")
print(f"Legenda criada: {slides_dir / 'legenda.txt'}")
print(f"Imagens carregadas: {len(slide_images)}")
