import base64
import json
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
TOTAL_SLIDES = 8
CONTACT_PHONE = "(81) 9 9864-5846"
CONTACT_EMAIL = "veronicabomfim.nutri@gmail.com"
CONTACT_WEBSITE = "https://veronicabomfimnutriweb.pages.dev/"


def load_image_base64(image_path):
    path = Path(image_path)
    if not path.exists():
        return None
    mime = "image/jpeg"
    if path.suffix.lower() == ".png":
        mime = "image/png"
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"


def get_capa_para_tema(tema):
    tracking = json.loads((BASE_DIR / "imagens_usadas.json").read_text(encoding="utf-8"))
    for entry in tracking.get("historico", []):
        if entry.get("tema") == tema:
            return BASE_DIR / "Imagens" / "nanobanana" / entry["imagem"]
    return escolher_imagem_capa(tema=tema)


img1_path = get_capa_para_tema("intestino-imunidade")
profile_data_uri = load_image_base64(img1_path) if img1_path else None

intestino_img_path = str(BASE_DIR / "slides" / "intestino-imunidade" / "intestino.jpg")
intestino_data_uri = load_image_base64(intestino_img_path) if Path(intestino_img_path).exists() else None

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


topic = "Eixo intestino-imunidade: sua saúde começa no intestino"
hook = "Mais de 70% das células de defesa do seu corpo vivem no intestino"

slide1_img = ""
if profile_data_uri:
    slide1_img = f'''<img src="{profile_data_uri}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;">
  <div style="position:absolute;inset:0;background:linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.6) 100%);z-index:1;"></div>'''

slides = []

# ============================================
# SLIDE 1 — CAPA
# ============================================
slides.append(f'''
<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 60px;overflow:hidden;position:relative;">
  {slide1_img}
  <div style="position:relative;z-index:2;">
    <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:16px;">IMUNIDADE & NUTRIÇÃO</span>
    <h1 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:700;color:#fff;line-height:1.1;margin:0 0 14px 0;">{topic}</h1>
    <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.85);line-height:1.5;margin:0 0 20px 0;">{hook}</p>
    <div style="display:flex;align-items:center;gap:12px;">
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

# ============================================
# SLIDE 2 — PROBLEMA (dado de impacto + foto intestino)
# ============================================
slide2_img = ""
if intestino_data_uri:
    slide2_img = f'''<img src="{intestino_data_uri}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center;z-index:0;">
  <div style="position:absolute;inset:0;background:linear-gradient(to bottom, rgba(57,66,51,0.85) 0%, rgba(57,66,51,0.55) 45%, rgba(57,66,51,0.9) 100%);z-index:1;"></div>'''

slides.append(f'''
<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:center;padding:0 36px;overflow:hidden;position:relative;">
  {slide2_img}
  <div style="position:relative;z-index:2;display:flex;flex-direction:column;">
    <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:18px;">O PROBLEMA</span>
    <h2 style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:600;color:#fff;line-height:1.18;margin:0 0 18px 0;">Onde mora a sua imunidade?</h2>
    <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.85);line-height:1.55;margin:0 0 18px 0;">Você sabe qual é o maior órgão imune do corpo? Não é o fígado nem o baço — é o intestino.</p>
    <div style="padding:18px 20px;background:rgba(0,0,0,0.35);border-left:3px solid {BRAND_PRIMARY};border-radius:6px;">
      <p style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.7);margin:0 0 6px 0;">A CIÊNCIA REVELA</p>
      <p style="font-family:'{FONT_HEADING}',serif;font-size:18px;color:#fff;font-weight:600;line-height:1.3;margin:0;">Entre 70% e 80% das células de defesa do corpo estão no tecido imune do intestino (GALT).</p>
    </div>
  </div>
  {swipe_arrow(False)}
</div>
''')

# ============================================
# SLIDE 3 — O QUE É O EIXO
# ============================================
slides.append(f'''
<div class="slide" style="background:linear-gradient(165deg, {BRAND_DARK} 0%, {BRAND_PRIMARY} 50%, {BRAND_LIGHT} 100%);display:flex;flex-direction:column;justify-content:center;padding:0 36px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:rgba(255,255,255,0.85);margin-bottom:18px;">O QUE ACONTECE NO CORPO</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:600;color:#fff;line-height:1.18;margin:0 0 22px 0;">Intestino e imunidade conversam o tempo todo</h2>
  <div style="display:flex;flex-direction:column;gap:14px;">
    <div style="padding:14px 16px;background:rgba(0,0,0,0.28);border-radius:10px;border:1px solid rgba(255,255,255,0.18);">
      <p style="font-family:'{FONT_BODY}',sans-serif;font-size:11px;color:rgba(255,255,255,0.7);margin:0 0 4px 0;letter-spacing:1px;">MICROBIOTA</p>
      <p style="font-family:'{FONT_HEADING}',serif;font-size:16px;color:#fff;font-weight:600;margin:0;">Trilhões de bactérias treinam e regulam sua resposta imune.</p>
    </div>
    <div style="padding:14px 16px;background:rgba(0,0,0,0.28);border-radius:10px;border:1px solid rgba(255,255,255,0.18);">
      <p style="font-family:'{FONT_BODY}',sans-serif;font-size:11px;color:rgba(255,255,255,0.7);margin:0 0 4px 0;letter-spacing:1px;">BARREIRA INTESTINAL</p>
      <p style="font-family:'{FONT_HEADING}',serif;font-size:16px;color:#fff;font-weight:600;margin:0;">Seleciona o que entra no corpo e mantém a defesa em equilíbrio.</p>
    </div>
  </div>
  {swipe_arrow(False)}
</div>
''')

# ============================================
# SLIDE 4 — SINAIS DE ALERTA
# ============================================
slides.append(f'''
<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:16px;">SINAIS DE ALERTA</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:600;color:#1e293b;line-height:1.18;margin:0 0 16px 0;">Sinais de que o intestino precisa de atenção</h2>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:#8A8580;line-height:1.55;margin:0 0 16px 0;">Quando a microbiota está desequilibrada, a imunidade sente:</p>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">✦</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#1e293b;display:block;">Gripes e resfriados frequentes</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Sua defesa fica mais lenta para reagir</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">✦</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#1e293b;display:block;">Digestão ruim, gases ou inchaço</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Sinal clássico de flora desequilibrada</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">✦</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#1e293b;display:block;">Cansaço e alterações de humor</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">O eixo intestino-cérebro também interfere</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">✦</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#1e293b;display:block;">Alergias e inflamações de repetição</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Resposta imune exagerada demais</span></div>
    </div>
  </div>
  {swipe_arrow(True)}
</div>
''')

# ============================================
# SLIDE 5 — O QUE FORTALECE A IMUNIDADE
# ============================================
slides.append(f'''
<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:center;padding:0 36px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:18px;">O QUE COMER</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:600;color:#fff;line-height:1.18;margin:0 0 22px 0;">O que nutre a sua imunidade</h2>
  <div style="display:flex;flex-direction:column;gap:10px;">
    <div style="display:flex;align-items:flex-start;gap:14px;padding:12px 16px;background:rgba(191,149,102,0.12);border:1px solid rgba(191,149,102,0.3);border-radius:10px;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:18px;color:{BRAND_PRIMARY};font-weight:700;min-width:28px;">1</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:#fff;font-weight:600;display:block;">Fibras (prebióticos)</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.6);">Alimentam as bactérias boas do intestino</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:12px 16px;background:rgba(191,149,102,0.12);border:1px solid rgba(191,149,102,0.3);border-radius:10px;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:18px;color:{BRAND_PRIMARY};font-weight:700;min-width:28px;">2</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:#fff;font-weight:600;display:block;">Alimentos fermentados</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.6);">Trazem bactérias vivas (probióticos)</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:12px 16px;background:rgba(191,149,102,0.12);border:1px solid rgba(191,149,102,0.3);border-radius:10px;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:18px;color:{BRAND_PRIMARY};font-weight:700;min-width:28px;">3</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:#fff;font-weight:600;display:block;">Variedade de plantas</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.6);">Quanto mais cores no prato, melhor para a flora</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:12px 16px;background:rgba(191,149,102,0.18);border:1px solid rgba(191,149,102,0.4);border-radius:10px;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:18px;color:{BRAND_PRIMARY};font-weight:700;min-width:28px;">4</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:#fff;font-weight:600;display:block;">Proteínas e zinco</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.6);">Matéria-prima das células de defesa</span></div>
    </div>
  </div>
  {swipe_arrow(False)}
</div>
''')

# ============================================
# SLIDE 6 — ESTRATÉGIAS PRÁTICAS
# ============================================
slides.append(f'''
<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:16px;">O QUE FAZER</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:600;color:#1e293b;line-height:1.18;margin:0 0 16px 0;">4 estratégias práticas no dia a dia</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:16px;padding:12px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:24px;font-weight:300;color:{BRAND_PRIMARY};min-width:32px;line-height:1;flex-shrink:0;">01</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#1e293b;display:block;">Feijão e leguminosas todos os dias</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Fibra que alimenta a flora saudável</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:16px;padding:12px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:24px;font-weight:300;color:{BRAND_PRIMARY};min-width:32px;line-height:1;flex-shrink:0;">02</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#1e293b;display:block;">Kefir ou iogurte natural</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Probióticos que calibram a resposta imune</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:16px;padding:12px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:24px;font-weight:300;color:{BRAND_PRIMARY};min-width:32px;line-height:1;flex-shrink:0;">03</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#1e293b;display:block;">20 a 30 plantas por semana</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Diversidade é proteção para a flora</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:16px;padding:12px 0;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:24px;font-weight:300;color:{BRAND_PRIMARY};min-width:32px;line-height:1;flex-shrink:0;">04</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#1e293b;display:block;">Reduza ultraprocessados e açúcar</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Eles alimentam bactérias menos benéficas</span></div>
    </div>
  </div>
  {swipe_arrow(True)}
</div>
''')

# ============================================
# SLIDE 7 — FECHAMENTO
# ============================================
slides.append(f'''
<div class="slide" style="background:linear-gradient(165deg, {BRAND_DARK} 0%, #5a6b4f 60%, {BRAND_PRIMARY} 100%);display:flex;flex-direction:column;justify-content:center;padding:0 36px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:rgba(255,255,255,0.85);margin-bottom:18px;">A MENSAGEM FINAL</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#fff;line-height:1.18;margin:0 0 18px 0;">Cuide do intestino e fortaleça a imunidade</h2>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.85);line-height:1.55;margin:0 0 22px 0;">Imunidade forte não é sorte — é o reflexo do que você come todos os dias.</p>
  <div style="padding:16px 18px;background:rgba(0,0,0,0.28);border-left:3px solid {BRAND_LIGHT};border-radius:6px;">
    <p style="font-family:'{FONT_HEADING}',serif;font-size:15px;color:#fff;font-style:italic;line-height:1.45;margin:0;">"O intestino não é só digestão: é onde grande parte da sua defesa é construída."</p>
  </div>
  {swipe_arrow(False)}
</div>
''')

# ============================================
# SLIDE 8 — CTA FINAL
# ============================================
cta_img_path = str(BASE_DIR / "Documento" / "Imagens" / "CTA" / "CTA.png")
cta_img_data_uri = None
if Path(cta_img_path).exists():
    b64 = base64.b64encode(Path(cta_img_path).read_bytes()).decode()
    cta_img_data_uri = f"data:image/png;base64,{b64}"
    print(f"✅ CTA image loaded: {len(b64)} chars")
else:
    print("⚠️  CTA.png not found, using fallback gradient")

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
      <span class="handle">{INSTA_HANDLE}</span> {hook} — cuidar do intestino é construir sua defesa. Veja o que a alimentação faz pela sua imunidade. #intestino #imunidade #microbiota #nutricaofuncional
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

output_file = str(BASE_DIR / "slides" / "intestino-imunidade" / "carousel.html")
slides_dir = Path(output_file).parent
slides_dir.mkdir(exist_ok=True)
Path(output_file).write_text(html, encoding="utf-8")

legenda = f"""{INSTA_HANDLE}

Eixo intestino-imunidade: sua saúde começa no intestino

📌 Descrição:
Você sabia que entre 70% e 80% das células de defesa do seu corpo vivem no intestino? O eixo intestino-imunidade mostra como a sua alimentação influencia diretamente a capacidade do organismo de se defender. Quando a microbiota intestinal está desequilibrada, gripes, alergias e inflamações ficam mais frequentes. Neste carrossel, explico por que o intestino é considerado o maior órgão imune, quais os sinais de alerta e o que comer para fortalecer a defesa no dia a dia.

📝 Resumo:
• Entre 70% e 80% das células imunes estão no tecido linfoide associado ao intestino (GALT)
• A microbiota e a barreira intestinal treinam e regulam a resposta de defesa
• Sinais de intestino desequilibrado: gripes frequentes, gases, inchaço, cansaço e alergias
• Fibras (prebióticos) e fermentados (probióticos) são essenciais para a flora saudável
• Variedade de plantas (20 a 30 por semana) e proteínas com zinco nutrem a imunidade
• Estratégias práticas: feijão diário, kefir/iogurte, mais plantas e menos ultraprocessados

📚 Fontes:
Estudos sobre microbiota e imunidade — The Journal of Immunology
Nature Reviews Immunology — eixo intestino-imunidade
Literatura de Nutrição Funcional e Imunonutrição
Guia Alimentar para a População Brasileira — Ministério da Saúde (OMS/OPAS)

🏷️ Hashtags:
#intestino #imunidade #microbiota #probióticos #prebioticos #nutricaofuncional #imunonutricao #saude #bemestar #alimentacaosaudavel #fibra #nutricionista #veronicabomfim #recife

📞 Contato:
📱 {CONTACT_PHONE}
📧 {CONTACT_EMAIL}
📸 {INSTA_HANDLE}
🌐 {CONTACT_WEBSITE}
"""

slides_dir.joinpath("legenda.txt").write_text(legenda, encoding="utf-8")

print(f"Carrossel criado: {output_file}")
print(f"Legenda criada: {slides_dir / 'legenda.txt'}")
print(f"Total de slides: {TOTAL_SLIDES}")