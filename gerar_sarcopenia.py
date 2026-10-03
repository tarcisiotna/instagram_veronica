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
TOTAL_SLIDES = 7

img1_path = escolher_imagem_capa(tema="perda-massa-magra-sarcopenia")

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
    <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:#fff;margin-bottom:16px;">SARCOPENIA</span>
    <h1 style="font-family:'{FONT_HEADING}',serif;font-size:30px;font-weight:700;color:#fff;line-height:1.1;margin:0 0 16px 0;">O inimigo silencioso que rouba sua força</h1>
    <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.9);line-height:1.5;margin:0 0 24px 0;">Perda de massa muscular não é só estética — é questão de saúde, autonomia e qualidade de vida.</p>
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
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 14px 0;">Sarcopenia: muito além da aparência</h2>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.7);line-height:1.5;margin:0 0 20px 0;">A perda progressiva de massa e força muscular afeta mobilidade, metabolismo e resposta ao tratamento oncológico. O pior: muitos só descobrem quando já está avançada.</p>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:4px;">
    <span style="font-size:11px;padding:5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:#94a3b8;text-decoration:line-through;">Acontece só em idosos</span>
    <span style="font-size:11px;padding:5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:#94a3b8;text-decoration:line-through;">Não tem como reverter</span>
    <span style="font-size:11px;padding:5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:#94a3b8;text-decoration:line-through;">Só exercício resolve</span>
  </div>
  {swipe_arrow(False)}
</div>''')

slides.append(f'''<div class="slide" style="background:linear-gradient(165deg, {BRAND_DARK} 0%, {BRAND_PRIMARY} 50%, {BRAND_LIGHT} 100%);display:flex;flex-direction:column;justify-content:center;padding:0 36px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:rgba(255,255,255,0.8);margin-bottom:16px;">A SOLUÇÃO</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:30px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 20px 0;">A nutrição é a chave para frear a sarcopenia</h2>
  <div style="padding:20px;background:rgba(0,0,0,0.25);border-radius:12px;border:1px solid rgba(255,255,255,0.15);margin-bottom:16px;">
    <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:rgba(255,255,255,0.7);margin:0 0 8px 0;">Dica da SBEM</p>
    <p style="font-family:'{FONT_HEADING}',serif;font-size:16px;color:#fff;font-style:italic;line-height:1.5;margin:0;">"Com intervenção nutricional adequada, é possível reverter a perda muscular e recuperar a força, mesmo durante o tratamento oncológico."</p>
  </div>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:rgba(255,255,255,0.8);line-height:1.5;margin:0;font-weight:600;">Evidências: SBEM, ESPEN, PubMed.</p>
  {swipe_arrow(False)}
</div>''')

slides.append(f'''<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:16px;">BENEFÍCIOS</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:{DARK_BG};line-height:1.15;margin:0 0 18px 0;">O que o acompanhamento nutricional proporciona</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">✦</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Preservação da massa magra</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Evita a perda muscular progressiva</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">✦</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Mais força e disposição</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Melhora da funcionalidade no dia a dia</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">✦</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Melhor resposta ao tratamento</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Paciente nutrido tolera melhor a quimio/radio</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">✦</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Qualidade de vida preservada</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Independência e autonomia por mais tempo</span></div>
    </div>
  </div>
  {swipe_arrow(True)}
</div>''')

slides.append(f'''<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:16px;">FATORES DE RISCO</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 14px 0;">Sarcopenia pode afetar todos</h2>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.6);line-height:1.5;margin:0 0 16px 0;">Conheça os principais fatores que aceleram a perda muscular:</p>
  <div style="display:flex;gap:8px;flex-wrap:wrap;">
    <span style="font-size:11px;padding:6px 14px;background:rgba(255,255,255,0.06);border-radius:20px;color:{BRAND_LIGHT};">Envelhecimento</span>
    <span style="font-size:11px;padding:6px 14px;background:rgba(255,255,255,0.06);border-radius:20px;color:{BRAND_LIGHT};">Câncer e tratamento</span>
    <span style="font-size:11px;padding:6px 14px;background:rgba(255,255,255,0.06);border-radius:20px;color:{BRAND_LIGHT};">Sedentarismo</span>
    <span style="font-size:11px;padding:6px 14px;background:rgba(255,255,255,0.06);border-radius:20px;color:{BRAND_LIGHT};">Baixa ingestão proteica</span>
    <span style="font-size:11px;padding:6px 14px;background:rgba(255,255,255,0.06);border-radius:20px;color:{BRAND_LIGHT};">Doenças crônicas</span>
    <span style="font-size:11px;padding:6px 14px;background:rgba(255,255,255,0.06);border-radius:20px;color:{BRAND_LIGHT};">Desnutrição</span>
  </div>
  {swipe_arrow(False)}
</div>''')

slides.append(f'''<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:16px;">PASSO A PASSO</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:{DARK_BG};line-height:1.15;margin:0 0 18px 0;">3 pilares para prevenir e tratar a sarcopenia</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">01</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Proteínas adequadas (1,2-2,0g/kg/dia)</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Distribuir ao longo do dia para estimular síntese muscular</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">02</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Leucina + Vitamina D</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Nutrientes essenciais para ativar a construção muscular</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">03</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Exercício resistido + acompanhamento</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Nutrição e atividade física andam juntos</span></div>
    </div>
  </div>
  {swipe_arrow(True)}
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
      <span class="handle">{INSTA_HANDLE}</span> O inimigo silencioso que rouba sua força! Perda de massa muscular não é só estética — é questão de saúde. Descubra como prevenir e tratar a sarcopenia. 💪🥗
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

output_dir = BASE_DIR / "slides" / "perda-massa-magra-sarcopenia"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "carousel.html"
output_path.write_text(html, encoding="utf-8")

html_size_mb = len(html.encode('utf-8')) / 1024 / 1024
print(f"✅ HTML gerado: {output_path}")
print(f"📦 Tamanho: {html_size_mb:.2f}MB")
print(f"🖼️  Imagem Slide 1: {img1_path.name if img1_path else 'Nenhuma'}")
print(f"📐 Total de slides: {TOTAL_SLIDES}")
print(f"\nAviso: As barras de progresso serão adicionadas pelo script de exportação.")
