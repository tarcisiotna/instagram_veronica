import base64
import random
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
TOTAL_SLIDES = 7

nanobanana_dir = BASE_DIR / "Imagens" / "nanobanana"
nanobanana_imgs = [p for p in list(nanobanana_dir.glob("*.jpeg")) + list(nanobanana_dir.glob("*.jpg")) if p.stat().st_size > 1_000_000]
img1_path = random.choice(nanobanana_imgs) if nanobanana_imgs else None

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
    <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:#fff;margin-bottom:16px;">HIGIENE DO SONO</span>
    <h1 style="font-family:'{FONT_HEADING}',serif;font-size:30px;font-weight:700;color:#fff;line-height:1.1;margin:0 0 16px 0;">Dormir bem é fundamental para vencer o câncer</h1>
    <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.9);line-height:1.5;margin:0 0 24px 0;">O sono de qualidade fortalece o sistema imunológico e melhora a resposta ao tratamento oncológico.</p>
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
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 14px 0;">Sono ruim prejudica o tratamento</h2>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.7);line-height:1.5;margin:0 0 20px 0;">O câncer é uma doença inflamatória. Quando o paciente não dorme bem, o cortisol aumenta e reduz as células de defesa Natural Killer, comprometendo a resposta ao tratamento.</p>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:4px;">
    <span style="font-size:11px;padding:5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:#94a3b8;text-decoration:line-through;">Sono não interfere no tratamento</span>
    <span style="font-size:11px;padding:5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:#94a3b8;text-decoration:line-through;">Dormir mal é normal durante a quimio</span>
    <span style="font-size:11px;padding:5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:#94a3b8;text-decoration:line-through;">Não tem como melhorar o sono</span>
  </div>
  {swipe_arrow(False)}
</div>''')

slides.append(f'''<div class="slide" style="background:linear-gradient(165deg, {BRAND_DARK} 0%, {BRAND_PRIMARY} 50%, {BRAND_LIGHT} 100%);display:flex;flex-direction:column;justify-content:center;padding:0 36px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:rgba(255,255,255,0.8);margin-bottom:16px;">A SOLUÇÃO</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:30px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 20px 0;">Sono de qualidade potencializa o tratamento</h2>
  <div style="padding:20px;background:rgba(0,0,0,0.25);border-radius:12px;border:1px solid rgba(255,255,255,0.15);margin-bottom:16px;">
    <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:rgba(255,255,255,0.7);margin:0 0 8px 0;">Estudo Journal of Cancer Research (2025)</p>
    <p style="font-family:'{FONT_HEADING}',serif;font-size:16px;color:#fff;font-style:italic;line-height:1.5;margin:0;">"Intervenções de sono combinadas com suporte nutricional melhoram significativamente a qualidade do sono, estado nutricional e qualidade de vida em pacientes oncológicos."</p>
  </div>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:rgba(255,255,255,0.8);line-height:1.5;margin:0;font-weight:600;">Evidências: PubMed, INCA, ESPEN.</p>
  {swipe_arrow(False)}
</div>''')

slides.append(f'''<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:16px;">ALIMENTOS</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:{DARK_BG};line-height:1.15;margin:0 0 18px 0;">O que comer para dormir melhor</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🥛</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Triptofano</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Leite, banana, grão de bico, ovos — precursor de serotonina e melatonina</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🥜</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Magnésio</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Amêndoas, castanhas, sementes, vegetais escuros — relaxa o sistema nervoso</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🍌</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Vitamina B6</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Banana, batata, frango — essencial para síntese de melatonina</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🍵</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Fitoterápicos</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Camomila, maracujá, melatonina — sempre com orientação profissional</span></div>
    </div>
  </div>
  {swipe_arrow(True)}
</div>''')

slides.append(f'''<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:16px;">DICAS PRÁTICAS</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 14px 0;">Higiene do sono na prática</h2>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.6);line-height:1.5;margin:0 0 16px 0;">Pequenas mudanças fazem grande diferença na qualidade do sono:</p>
  <div style="display:flex;gap:8px;flex-wrap:wrap;">
    <span style="font-size:11px;padding:6px 14px;background:rgba(255,255,255,0.06);border-radius:20px;color:{BRAND_LIGHT};">Ambiente escuro e silencioso</span>
    <span style="font-size:11px;padding:6px 14px;background:rgba(255,255,255,0.06);border-radius:20px;color:{BRAND_LIGHT};">Sem telas 1h antes de dormir</span>
    <span style="font-size:11px;padding:6px 14px;background:rgba(255,255,255,0.06);border-radius:20px;color:{BRAND_LIGHT};">Evitar cafeína à noite</span>
    <span style="font-size:11px;padding:6px 14px;background:rgba(255,255,255,0.06);border-radius:20px;color:{BRAND_LIGHT};">Jantar leve e cedo</span>
    <span style="font-size:11px;padding:6px 14px;background:rgba(255,255,255,0.06);border-radius:20px;color:{BRAND_LIGHT};">Horários regulares</span>
    <span style="font-size:11px;padding:6px 14px;background:rgba(255,255,255,0.06);border-radius:20px;color:{BRAND_LIGHT};">Atividade física moderada</span>
    <span style="font-size:11px;padding:6px 14px;background:rgba(255,255,255,0.06);border-radius:20px;color:{BRAND_LIGHT};">Evitar cochilos longos</span>
    <span style="font-size:11px;padding:6px 14px;background:rgba(255,255,255,0.06);border-radius:20px;color:{BRAND_LIGHT};">Mantenha o quarto fresco</span>
  </div>
  {swipe_arrow(False)}
</div>''')

slides.append(f'''<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:16px;">PASSO A PASSO</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:{DARK_BG};line-height:1.15;margin:0 0 18px 0;">3 passos para uma noite de sono reparador</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">01</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Prepare o ambiente</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Quarto escuro, silencioso, fresco. Sem celular ou TV antes de dormir</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">02</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Alimente-se estrategicamente</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Jantar leve com triptofano (banana, leite, ovos). Evitar estimulantes à noite</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">03</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Crie uma rotina</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Dormir e acordar no mesmo horário. Relaxar antes com chá ou leitura leve</span></div>
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
      <span class="handle">{INSTA_HANDLE}</span> Dormir bem é fundamental para vencer o câncer! Descubra como a higiene do sono fortalece o sistema imunológico e melhora a resposta ao tratamento oncológico. 😴🥗
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

output_dir = BASE_DIR / "slides" / "higiene-do-sono"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "carousel.html"
output_path.write_text(html, encoding="utf-8")

legenda = f"""{INSTA_HANDLE}

Higiene do Sono: Dormir bem é fundamental para vencer o câncer

📌 Descrição:
O sono de qualidade é um dos pilares mais importantes para o sucesso do tratamento oncológico. Quando o paciente não dorme bem, o cortisol aumenta e as células de defesa do sistema imunológico diminuem, comprometendo a resposta à quimioterapia e radioterapia. Neste carrossel, você vai entender a ciência por trás do sono, quais alimentos ajudam a dormir melhor e dicas práticas de higiene do sono.

📝 Resumo:
• O sono ruim eleva o cortisol e reduz as células Natural Killer, prejudicando a resposta ao tratamento
• Alimentos ricos em triptofano (leite, banana, ovos) ajudam na produção de melatonina
• Magnésio, vitamina B6 e fitoterápicos como camomila auxiliam o relaxamento
• Ambiente escuro, sem telas e horários regulares são essenciais para um sono reparador
• Estudo de 2025 (Journal of Cancer Research) comprova: sono + nutrição melhoram qualidade de vida

📚 Fontes:
INCA — Instituto Nacional de Câncer
PubMed — Journal of Cancer Research and Clinical Oncology (2025)
ESPEN — Diretrizes Europeias de Nutrição Clínica
SBNO — Sociedade Brasileira de Nutrição Oncológica

🏷️ Hashtags:
#higienedosono #sono #nutricao #oncologia #cancer #tratamentooncologico #sonosaudavel #imunidade #nutricionista #veronicabomfim #recife #saude #melatonina #triptofano

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
