import base64
import random
from pathlib import Path

# Imagens - Slide 1: foto aleatória da pasta nanobanana
nanobanana_dir = Path("/home/tarcisio/instagram_veronica/Imagens/nanobanana")
nanobanana_imgs = list(nanobanana_dir.glob("*.jpeg"))
img1_path = random.choice(nanobanana_imgs) if nanobanana_imgs else None

# Slide 7 (CTA): sempre usar CTA.png
img_cta_path = Path("/home/tarcisio/instagram_veronica/Imagens/CTA/CTA.png")

def encode_img(path):
    if not path or not path.exists():
        return None
    mime = "image/jpeg" if str(path).endswith(".jpeg") else "image/png"
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"

img1_b64 = encode_img(img1_path)
img_cta_b64 = encode_img(img_cta_path)

# Cores do guia da marca (Documento/Guia da marca.md)
PRIMARY = "#bf9566"  # gold/brown
LIGHT = "#ecd7ba"    # light cream
DARK = "#394233"     # dark slate
LIGHT_BG = "#FAF9F7"  # warm off-white
LIGHT_BORDER = "#ecd7ba"
DARK_BG = "#394233"    # dark slate

# Google Fonts - Playfair Display (heading) + TT Norms (body)
FONTS_LINK = '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">'

def progress_bar(index, total, is_light):
    pct = ((index + 1) / total) * 100
    track = "rgba(0,0,0,0.08)" if is_light else "rgba(255,255,255,0.12)"
    fill = PRIMARY if is_light else "#fff"
    label = "rgba(0,0,0,0.3)" if is_light else "rgba(255,255,255,0.4)"
    return (f'<div style="position:absolute;bottom:0;left:0;right:0;padding:16px 28px 20px;z-index:10;'
            f'display:flex;align-items:center;gap:10px;">'
            f'<div style="flex:1;height:3px;background:{track};border-radius:2px;overflow:hidden;">'
            f'<div style="height:100%;width:{pct}%;background:{fill};border-radius:2px;"></div></div>'
            f'<span style="font-size:11px;color:{label};font-weight:500;">{index+1}/{total}</span></div>')

def swipe_arrow(is_light):
    bg = "rgba(0,0,0,0.06)" if is_light else "rgba(255,255,255,0.08)"
    stroke = "rgba(0,0,0,0.25)" if is_light else "rgba(255,255,255,0.35)"
    return (f'<div style="position:absolute;right:0;top:0;bottom:0;width:48px;z-index:9;'
            f'display:flex;align-items:center;justify-content:center;'
            f'background:linear-gradient(to right,transparent,{bg});">'
            f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none">'
            f'<path d="M9 6l6 6-6 6" stroke="{stroke}" stroke-width="2.5" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg></div>')

TOTAL = 7
slides = []

# Slide 1 - Hero com foto aleatória do nanobanana
img1_html = f'<img src="{img1_b64}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;opacity:0.18;">' if img1_b64 else ''
slides.append(
f'<div style="position:relative;width:420px;height:525px;background:{LIGHT_BG};flex-shrink:0;overflow:hidden;'
f'display:flex;flex-direction:column;justify-content:center;padding:0 36px;box-sizing:border-box;">'
f'{img1_html}'
f'<div style="position:relative;z-index:2;">'
f'<span class="sans" style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;'
f'color:{PRIMARY};margin-bottom:16px;">NUTRIÇÃO ONCOLÓGICA</span>'
f'<h1 class="serif" style="font-size:32px;font-weight:600;color:{DARK_BG};line-height:1.1;'
f'margin:0 0 18px 0;">A nutrição certa pode ser a diferença entre vencer ou não o tratamento</h1>'
f'<p class="sans" style="font-size:14px;color:#8A8580;line-height:1.5;margin:0;">'
f'Saiba como a alimentação impacta diretamente sua resposta à quimio e radioterapia.</p>'
f'</div>{progress_bar(0,TOTAL,True)}{swipe_arrow(True)}</div>')

# Slide 2
slides.append(
f'<div style="position:relative;width:420px;height:525px;background:{DARK_BG};flex-shrink:0;overflow:hidden;'
f'display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;box-sizing:border-box;">'
f'<div style="position:relative;z-index:2;">'
f'<span class="sans" style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;'
f'color:{LIGHT};margin-bottom:16px;">O PROBLEMA</span>'
f'<h2 class="serif" style="font-size:28px;font-weight:600;color:#fff;line-height:1.15;'
f'margin:0 0 18px 0;">Até 80% dos pacientes enfrentam desnutrição durante o tratamento</h2>'
f'<p class="sans" style="font-size:14px;color:rgba(255,255,255,0.7);line-height:1.5;margin:0 0 20px 0;">'
f'Náuseas, perda de apetite e efeitos colaterais afetam a ingestão, comprometendo a resposta terapêutica.</p>'
f'<div style="padding:14px;background:rgba(255,255,255,0.06);border-radius:10px;'
f'border:1px solid rgba(255,255,255,0.08);">'
f'<p class="sans" style="font-size:12px;color:rgba(255,255,255,0.5);margin:0;">'
f'Fonte: INCA — Guia de Nutrição para Pacientes e Cuidadores</p></div>'
f'</div>{progress_bar(1,TOTAL,False)}{swipe_arrow(False)}</div>')

# Slide 3
slides.append(
f'<div style="position:relative;width:420px;height:525px;'
f'background:linear-gradient(165deg,{DARK} 0%,{PRIMARY} 50%,{LIGHT} 100%);flex-shrink:0;overflow:hidden;'
f'display:flex;flex-direction:column;justify-content:center;padding:0 36px;box-sizing:border-box;">'
f'<div style="position:relative;z-index:2;">'
f'<span class="sans" style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;'
f'color:rgba(255,255,255,0.6);margin-bottom:16px;">A SOLUÇÃO</span>'
f'<h2 class="serif" style="font-size:28px;font-weight:600;color:#fff;line-height:1.15;'
f'margin:0 0 18px 0;">Acompanhamento nutricional especializado</h2>'
f'<p class="sans" style="font-size:14px;color:rgba(255,255,255,0.8);line-height:1.5;margin:0 0 24px 0;">'
f'A nutrição oncológica previne a perda de peso, melhora a tolerância ao tratamento e reduz complicações.</p>'
f'<div style="padding:16px;background:rgba(0,0,0,0.15);border-radius:12px;'
f'border:1px solid rgba(255,255,255,0.08);">'
f'<p class="sans" style="font-size:13px;color:rgba(255,255,255,0.5);margin-bottom:6px;">SBNO recomenda</p>'
f'<p class="serif" style="font-size:15px;color:#fff;font-style:italic;line-height:1.4;margin:0;">'
f'"O acompanhamento nutricional deve ser iniciado assim que o diagnóstico é confirmado."</p></div>'
f'</div>{progress_bar(2,TOTAL,False)}{swipe_arrow(False)}</div>')

# Slide 4
slides.append(
f'<div style="position:relative;width:420px;height:525px;background:{LIGHT_BG};flex-shrink:0;overflow:hidden;'
f'display:flex;flex-direction:column;justify-content:center;padding:0 36px;box-sizing:border-box;">'
f'<div style="position:relative;z-index:2;">'
f'<span class="sans" style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;'
f'color:{PRIMARY};margin-bottom:16px;">BENEFÍCIOS</span>'
f'<h2 class="serif" style="font-size:28px;font-weight:600;color:{DARK_BG};line-height:1.15;'
f'margin:0 0 24px 0;">O que o acompanhamento traz</h2>'
f'<div style="display:flex;flex-direction:column;gap:2px;">'
f'<div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">'
f'<span style="color:{PRIMARY};font-size:15px;width:18px;text-align:center;">✦</span>'
f'<div><span class="sans" style="font-size:14px;font-weight:600;color:{DARK_BG};">Menor perda de peso</span>'
f'<br><span class="sans" style="font-size:12px;color:#8A8580;">Mantenha sua reserva energética durante o tratamento</span></div></div>'
f'<div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">'
f'<span style="color:{PRIMARY};font-size:15px;width:18px;text-align:center;">✦</span>'
f'<div><span class="sans" style="font-size:14px;font-weight:600;color:{DARK_BG};">Melhor resposta terapêutica</span>'
f'<br><span class="sans" style="font-size:12px;color:#8A8580;">Organismo fortalecido tolera melhor quimio e radioterapia</span></div></div>'
f'<div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">'
f'<span style="color:{PRIMARY};font-size:15px;width:18px;text-align:center;">✦</span>'
f'<div><span class="sans" style="font-size:14px;font-weight:600;color:{DARK_BG};">Controle de sintomas</span>'
f'<br><span class="sans" style="font-size:12px;color:#8A8580;">Redução de náuseas, fadiga e mucosite</span></div></div>'
f'<div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;">'
f'<span style="color:{PRIMARY};font-size:15px;width:18px;text-align:center;">✦</span>'
f'<div><span class="sans" style="font-size:14px;font-weight:600;color:{DARK_BG};">Qualidade de vida</span>'
f'<br><span class="sans" style="font-size:12px;color:#8A8580;">Mais energia e disposição no dia a dia</span></div></div>'
f'</div></div>{progress_bar(3,TOTAL,True)}{swipe_arrow(True)}</div>')

# Slide 5
slides.append(
f'<div style="position:relative;width:420px;height:525px;background:{DARK_BG};flex-shrink:0;overflow:hidden;'
f'display:flex;flex-direction:column;justify-content:center;padding:0 36px;box-sizing:border-box;">'
f'<div style="position:relative;z-index:2;">'
f'<span class="sans" style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;'
f'color:{LIGHT};margin-bottom:16px;">POR QUE ACONTECE</span>'
f'<h2 class="serif" style="font-size:28px;font-weight:600;color:#fff;line-height:1.15;'
f'margin:0 0 18px 0;">O câncer aumenta as necessidades nutricionais</h2>'
f'<p class="sans" style="font-size:14px;color:rgba(255,255,255,0.7);line-height:1.5;margin:0 0 20px 0;">'
f'O metabolismo acelerado pelo tumor e os efeitos do tratamento exigem mais calorias e proteínas do que o corpo normalmente precisa.</p>'
f'<div style="display:flex;gap:12px;flex-wrap:wrap;">'
f'<span style="font-size:11px;padding:5px 12px;background:rgba(255,255,255,0.06);border-radius:20px;color:{LIGHT};">+ Calorias</span>'
f'<span style="font-size:11px;padding:5px 12px;background:rgba(255,255,255,0.06);border-radius:20px;color:{LIGHT};">+ Proteínas</span>'
f'<span style="font-size:11px;padding:5px 12px;background:rgba(255,255,255,0.06);border-radius:20px;color:{LIGHT};">Hidratação</span>'
f'<span style="font-size:11px;padding:5px 12px;background:rgba(255,255,255,0.06);border-radius:20px;color:{LIGHT};">Micronutrientes</span>'
f'</div></div>{progress_bar(4,TOTAL,False)}{swipe_arrow(False)}</div>')

# Slide 6
slides.append(
f'<div style="position:relative;width:420px;height:525px;background:{LIGHT_BG};flex-shrink:0;overflow:hidden;'
f'display:flex;flex-direction:column;justify-content:center;padding:0 36px;box-sizing:border-box;">'
f'<div style="position:relative;z-index:2;">'
f'<span class="sans" style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;'
f'color:{PRIMARY};margin-bottom:16px;">PASSO A PASSO</span>'
f'<h2 class="serif" style="font-size:28px;font-weight:600;color:{DARK_BG};line-height:1.15;'
f'margin:0 0 24px 0;">Como funciona o acompanhamento</h2>'
f'<div style="display:flex;flex-direction:column;gap:2px;">'
f'<div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;border-bottom:1px solid {LIGHT_BORDER};">'
f'<span class="serif" style="font-size:26px;font-weight:300;color:{PRIMARY};min-width:34px;line-height:1;">01</span>'
f'<div><span class="sans" style="font-size:14px;font-weight:600;color:{DARK_BG};">Avaliação nutricional</span>'
f'<br><span class="sans" style="font-size:12px;color:#8A8580;">Diagnóstico do estado nutricional atual</span></div></div>'
f'<div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;border-bottom:1px solid {LIGHT_BORDER};">'
f'<span class="serif" style="font-size:26px;font-weight:300;color:{PRIMARY};min-width:34px;line-height:1;">02</span>'
f'<div><span class="sans" style="font-size:14px;font-weight:600;color:{DARK_BG};">Plano alimentar individualizado</span>'
f'<br><span class="sans" style="font-size:12px;color:#8A8580;">Adaptado aos sintomas e preferências</span></div></div>'
f'<div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;">'
f'<span class="serif" style="font-size:26px;font-weight:300;color:{PRIMARY};min-width:34px;line-height:1;">03</span>'
f'<div><span class="sans" style="font-size:14px;font-weight:600;color:{DARK_BG};">Monitoramento contínuo</span>'
f'<br><span class="sans" style="font-size:12px;color:#8A8580;">Ajustes conforme a resposta ao tratamento</span></div></div>'
f'</div></div>{progress_bar(5,TOTAL,True)}{swipe_arrow(True)}</div>')

# Slide 7 - CTA (apenas CTA.png como fundo)
slides.append(
f'<div style="position:relative;width:420px;height:525px;flex-shrink:0;overflow:hidden;">'
f'<img src="{img_cta_b64}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;">'
f'{progress_bar(6,TOTAL,False)}</div>')

# HTML completo
html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=420">
{FONTS_LINK}
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#1a1a1a;padding:40px 0;font-family:Inter,sans-serif;display:flex;justify-content:center;}}
.ig-frame{{width:420px;background:#000;border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,0.5);overflow:hidden;}}
.ig-header{{display:flex;align-items:center;gap:12px;padding:14px 16px;background:#000;color:#fff;}}
.ig-avatar{{width:40px;height:40px;border-radius:50%;background:{PRIMARY};display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:18px;}}
.ig-handle{{font-size:14px;font-weight:600;}}
.ig-sub{{font-size:11px;color:rgba(255,255,255,0.5);}}
.carousel-viewport{{width:420px;height:525px;overflow:hidden;position:relative;cursor:grab;}}
.carousel-track{{display:flex;transition:transform 0.4s ease;}}
.ig-dots{{display:flex;justify-content:center;gap:6px;padding:12px;background:#000;}}
.ig-dots span{{width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,0.3);}}
.ig-dots span.active{{background:#fff;}}
.ig-actions{{display:flex;gap:16px;padding:12px 16px;background:#000;color:#fff;}}
.ig-caption{{padding:8px 16px 16px;background:#000;color:#fff;font-size:13px;}}
.ig-caption .handle{{font-weight:600;}}
.ig-caption .time{{color:rgba(255,255,255,0.4);font-size:11px;}}
.serif{{font-family:Playfair Display,serif;}}
.sans{{font-family:Inter,sans-serif;}}
</style>
</head>
<body>
<div class="ig-frame">
<div class="ig-header">
<div class="ig-avatar">V</div>
<div><div class="ig-handle">@veronicabomfim.nutri</div><div class="ig-sub">Nutricionista Oncológica</div></div>
</div>
<div class="carousel-viewport" id="viewport">
<div class="carousel-track" id="track">
{''.join(slides)}
</div>
</div>
<div class="ig-dots" id="dots">
<span class="active"></span><span></span><span></span><span></span><span></span><span></span><span></span>
</div>
<div class="ig-actions">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" style="margin-left:auto;"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
</div>
<div class="ig-caption">
<span class="handle">@veronicabomfim.nutri</span> Nutrição no tratamento oncológico: a alimentação certa faz diferença na sua resposta ao tratamento. 🥗<br>
<span class="time">2 HOURS AGO</span>
</div>
</div>
<script>
let idx=0;const total={TOTAL};const track=document.getElementById('track');
const dots=document.getElementById('dots').children;
const viewport=document.getElementById('viewport');
function goTo(i){{idx=Math.max(0,Math.min(i,total-1));track.style.transform='translateX('+(-idx*420)+'px)';
Array.from(dots).forEach((d,j)=>d.classList.toggle('active',j===idx));}}
let startX=0;viewport.addEventListener('mousedown',e=>{{startX=e.clientX;}});
viewport.addEventListener('mouseup',e=>{{if(e.clientX-startX<-40)goTo(idx+1);else if(e.clientX-startX>40)goTo(idx-1);}});
let touchX=0;viewport.addEventListener('touchstart',e=>{{touchX=e.touches[0].clientX;}});
viewport.addEventListener('touchend',e=>{{const dx=e.changedTouches[0].clientX-touchX;
if(dx<-40)goTo(idx+1);else if(dx>40)goTo(idx-1);}});
</script>
</body>
</html>'''

# Salvar na pasta correta
slides_dir = Path("/home/tarcisio/instagram_veronica/slides/nutricao-oncologica")
slides_dir.mkdir(parents=True, exist_ok=True)
output_path = slides_dir / "carousel.html"
output_path.write_text(html, encoding="utf-8")
print(f"HTML gerado: {output_path}")
print(f"Imagem Slide 1: {img1_path.name if img1_path else 'Nenhuma'}")
print("Cores atualizadas conforme Documento/Guia da marca.md")
