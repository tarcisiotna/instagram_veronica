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
TOTAL_SLIDES = 8

img1_path = escolher_imagem_capa(tema="magnesio-e-o-sono")

cta_path = BASE_DIR / "Imagens" / "CTA" / "CTA.png"

logo_paths = [
    BASE_DIR / "Imagens" / "Sem fundo" / "1.png",
    BASE_DIR / "Imagens" / "Sem fundo" / "2.png",
    BASE_DIR / "Imagens" / "Sem fundo" / "3.png",
    BASE_DIR / "Imagens" / "Sem fundo" / "4.png",
    BASE_DIR / "Imagens" / "Sem fundo" / "5.png",
    BASE_DIR / "Imagens" / "Sem fundo" / "6.png",
    BASE_DIR / "Imagens" / "Sem fundo" / "7.png",
    BASE_DIR / "Imagens" / "Sem fundo" / "8.png",
    BASE_DIR / "Imagens" / "Sem fundo" / "9.png",
]

def encode_img(path):
    if not path or not path.exists():
        return None
    mime = "image/jpeg" if path.suffix.lower() in (".jpeg", ".jpg") else "image/png"
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"

img1_b64 = encode_img(img1_path)
cta_b64 = encode_img(cta_path)
logo_b64 = encode_img(logo_paths[0])

def swipe_arrow(is_light):
    bg = "rgba(0,0,0,0.06)" if is_light else "rgba(255,255,255,0.08)"
    stroke = "rgba(0,0,0,0.25)" if is_light else "rgba(255,255,255,0.35)"
    return f'''<div style="position:absolute;right:0;top:0;bottom:0;width:48px;z-index:9;display:flex;align-items:center;justify-content:center;background:linear-gradient(to right,transparent,{bg});">
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="{stroke}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
</div>'''

slides = []

img1_html = ""
if img1_b64:
    img1_html = f'<img src="{img1_b64}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;"><div style="position:absolute;inset:0;background:linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.7) 100%);z-index:1;"></div>'

slides.append(f'''<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:center;padding:0 36px;overflow:hidden;position:relative;">
  {img1_html}
  <div style="position:relative;z-index:2;">
    <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:#fff;margin-bottom:16px;">MAGNÉSIO E O SONO</span>
    <h1 style="font-family:'{FONT_HEADING}',serif;font-size:30px;font-weight:700;color:#fff;line-height:1.1;margin:0 0 16px 0;">O mineral mais buscado para dormir melhor</h1>
    <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.9);line-height:1.5;margin:0 0 24px 0;">Magnésio glicinato: o que a ciência diz sobre o suplemento que virou febre nas redes.</p>
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

slides.append(f'''<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:16px;">O PROBLEMA</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 14px 0;">Sinais de que falta magnésio</h2>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.7);line-height:1.5;margin:0 0 16px 0;">Cãibras noturnas, fadiga, dificuldade para dormir e estresse podem indicar deficiência.</p>
  <div style="padding:18px;background:rgba(255,255,255,0.06);border-radius:12px;border:1px solid rgba(255,255,255,0.1);margin-bottom:18px;">
    <span style="font-family:'{FONT_HEADING}',serif;font-size:30px;font-weight:700;color:{BRAND_PRIMARY};display:block;">2 em cada 3</span>
    <span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.6);">adultos não atingem a dose diária recomendada de magnésio</span>
  </div>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:4px;">
    <span style="font-size:11px;padding:5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:#94a3b8;">Cãibras à noite</span>
    <span style="font-size:11px;padding:5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:#94a3b8;">Fadiga constante</span>
    <span style="font-size:11px;padding:5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:#94a3b8;">Insônia e sono leve</span>
    <span style="font-size:11px;padding:5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:#94a3b8;">Estresse e ansiedade</span>
  </div>
  {swipe_arrow(False)}
</div>''')

slides.append(f'''<div class="slide" style="background:linear-gradient(165deg, {BRAND_DARK} 0%, {BRAND_PRIMARY} 50%, {BRAND_LIGHT} 100%);display:flex;flex-direction:column;justify-content:center;padding:0 36px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:rgba(255,255,255,0.8);margin-bottom:16px;">A CIÊNCIA</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:30px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 20px 0;">Por que o magnésio ajuda a dormir</h2>
  <div style="padding:20px;background:rgba(0,0,0,0.25);border-radius:12px;border:1px solid rgba(255,255,255,0.15);margin-bottom:16px;">
    <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:rgba(255,255,255,0.7);margin:0 0 8px 0;">Estudos clínicos</p>
    <p style="font-family:'{FONT_HEADING}',serif;font-size:16px;color:#fff;font-style:italic;line-height:1.5;margin:0;">"O magnésio regula a produção de melatonina e ativa os receptores GABA, que acalmam o sistema nervoso e preparam o corpo para o descanso."</p>
  </div>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:rgba(255,255,255,0.8);line-height:1.5;margin:0 0 12px 0;">Participa de mais de 600 reações no organismo. Em idosos com insônia, 250–500mg por 6–8 semanas melhoraram o início, a duração e a qualidade do sono.</p>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:rgba(255,255,255,0.8);line-height:1.5;margin:0;font-weight:600;">Evidências: ensaios clínicos com placebo, revisões científicas.</p>
  {swipe_arrow(False)}
</div>''')

slides.append(f'''<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:16px;">ALIMENTOS</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:{DARK_BG};line-height:1.15;margin:0 0 18px 0;">Onde encontrar magnésio</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🎃</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Sementes de abóbora</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Fonte mais concentrada: cerca de 150mg em 30g</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🥬</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Espinafre e acelga</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Folhas verde-escuras: ótimas no jantar</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🥜</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Amêndoas e castanhas</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Práticas como lanche ao longo do dia</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🍫</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Chocolate amargo 70-85%</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Fonte concentrada — 1 a 2 quadradinhos</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🫘</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Feijão preto, quinoa, abacate</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Presentes no prato brasileiro e fáceis de incluir</span></div>
    </div>
  </div>
  {swipe_arrow(True)}
</div>''')

slides.append(f'''<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:16px;">QUAL ESCOLHER</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 14px 0;">Nem todo magnésio é igual</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.08);">
      <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">✅</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Glicinato (bisglicinato)</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Melhor para sono e relaxamento — bem absorvido</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.08);">
      <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">⚖️</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Citrato</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Boa absorção, mas efeito laxativo em doses altas</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.08);">
      <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🧠</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Treonato</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Bom para cognição e foco — mais caro</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;">
      <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">⚠️</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Óxido</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Barato, mas mal absorvido — evite para o sono</span></div>
    </div>
  </div>
  <div style="padding:14px 16px;background:{BRAND_PRIMARY};border-radius:10px;margin-top:14px;">
    <span style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;font-weight:600;color:#fff;">Para dormir: glicinato é a forma mais recomendada 💛</span>
  </div>
  {swipe_arrow(False)}
</div>''')

slides.append(f'''<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:16px;">COMO USAR</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:{DARK_BG};line-height:1.15;margin:0 0 14px 0;">Na prática</h2>
  <div style="display:flex;flex-direction:column;gap:10px;">
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">01</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Dose: 200–400mg de magnésio elementar</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">1–2 horas antes de deitar</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">02</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Leia o rótulo</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">"1000mg de glicinato" ≈ 140mg de magnésio elementar</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">03</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Paciência: 3–7 dias</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Efeitos no sono aparecem com uso consistente</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">04</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Interações: cuidado!</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Separar 2h de antibióticos e remédios de pressão</span></div>
    </div>
  </div>
  {swipe_arrow(True)}
</div>''')

slides.append(f'''<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:16px;">MITO OU VERDADE?</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 16px 0;">Magnésio é a solução para a insônia?</h2>
  <div style="display:flex;flex-direction:column;gap:10px;margin-bottom:16px;">
    <div style="padding:14px 16px;background:rgba(255,255,255,0.06);border-radius:10px;border:1px solid rgba(255,255,255,0.1);">
      <span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;font-weight:600;color:#94a3b8;display:block;letter-spacing:1px;">MITO</span>
      <span style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:rgba(255,255,255,0.7);">Acreditar que resolve tudo sozinho ou substitui tratamento e higiene do sono</span>
    </div>
    <div style="padding:14px 16px;background:rgba(191,149,102,0.12);border-radius:10px;border:1px solid {BRAND_PRIMARY};">
      <span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;font-weight:600;color:{BRAND_LIGHT};display:block;letter-spacing:1px;">VERDADE</span>
      <span style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:#fff;">Ajuda quem tem deficiência ou baixa ingestão — como estratégia complementar, não milagre</span>
    </div>
  </div>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.8);line-height:1.5;margin:0;font-weight:600;">Magnésio + higiene do sono + orientação profissional = resultado real 🌙</p>
  {swipe_arrow(False)}
</div>''')

logo_img_tag = ""
if logo_b64:
    logo_img_tag = f'<img src="{logo_b64}" style="width:160px;height:auto;margin:0 auto 20px;filter:drop-shadow(0 8px 25px rgba(191,149,102,0.6));">'
else:
    logo_img_tag = f'<div style="width:100px;height:100px;border-radius:50%;background:{BRAND_PRIMARY};display:flex;align-items:center;justify-content:center;color:#fff;font-size:42px;font-weight:700;margin:0 auto 20px;box-shadow:0 8px 30px rgba(191,149,102,0.6);border:4px solid rgba(255,255,255,0.4);">V</div>'

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
      <span class="handle">{INSTA_HANDLE}</span> O mineral mais buscado para dormir melhor: magnésio glicinato! Descubra o que a ciência diz, onde encontrar e como usar. 😴💛 #magnesio #sono
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

output_dir = BASE_DIR / "slides" / "magnesio-e-o-sono"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "carousel.html"
output_path.write_text(html, encoding="utf-8")

legenda = f"""{INSTA_HANDLE}

Magnésio e o Sono: o mineral mais buscado para dormir melhor

📌 Descrição:
O magnésio se tornou a maior tendência de sono em 2026 — e não por acaso. Ele participa de mais de 600 reações no organismo, regula a produção de melatonina e ativa os receptores GABA, que acalmam o sistema nervoso. Neste carrossel, você vai entender por que quase 2 em cada 3 adultos não atingem a dose diária, quais alimentos são ricos em magnésio, como escolher a forma certa (spoiler: glicinato) e como usar com segurança — sem cair no mito do "milagre da insônia".

📝 Resumo:
• 2 em cada 3 adultos não atingem a dose diária recomendada de magnésio (310–420mg)
• O magnésio regula a melatonina e ativa os receptores GABA, ajudando no relaxamento e no sono
• Alimentos ricos: sementes de abóbora, espinafre, amêndoas, chocolate amargo 70%, feijão preto, abacate
• Para dormir, o glicinato é a forma mais recomendada — bem absorvido e suave para o intestino
• Dose: 200–400mg de magnésio elementar à noite; leia o rótulo (1000mg de glicinato ≈ 140mg elementar)
• Não é milagre: é estratégia complementar à higiene do sono, sempre com orientação profissional

📚 Fontes:
PubMed — estudos clínicos sobre magnésio e sono
NHANES — dados de ingestão de magnésio na população
Journal of Clinical Endocrinology & Metabolism — mecanismos da melatonina
Conselho Nacional de Saúde e literatura científica revisada

🏷️ Hashtags:
#magnesio #magnesioglicinato #sono #insonia #higienedosono #suplementacao #nutricao #dormirmelhor #saude #bemestar #magnesioparasono #nutricionista #veronicabomfim #recife

📞 Contato:
📱 {CONTACT_PHONE}
📧 {CONTACT_EMAIL}
📸 {INSTA_HANDLE}
🌐 https://veronicabomfimnutriweb.pages.dev/"""

output_dir.joinpath("legenda.txt").write_text(legenda, encoding="utf-8")

html_size_mb = len(html.encode('utf-8')) / 1024 / 1024
print(f"✅ HTML gerado: {output_path}")
print(f"📦 Tamanho: {html_size_mb:.2f}MB")
print(f"🖼️  Imagem Slide 1: {img1_path.name if img1_path else 'Nenhuma'}")
print(f"📐 Total de slides: {TOTAL_SLIDES}")
print(f"📝 Legenda criada: {output_dir / 'legenda.txt'}")
print(f"\nAviso: As barras de progresso serão adicionadas pelo script de exportação.")
