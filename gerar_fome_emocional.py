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

img1_path = escolher_imagem_capa(tema="fome-fisica-vs-fome-emocional")

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
  {img1_html}
  <div style="position:relative;z-index:2;">
    <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:14px;background:rgba(57,66,51,0.55);padding:6px 12px;border-radius:20px;">NUTRIÇÃO COMPORTAMENTAL</span>
    <h1 style="font-family:'{FONT_HEADING}',serif;font-size:33px;font-weight:700;color:#fff;line-height:1.1;margin:0 0 14px 0;">Fome física vs fome emocional</h1>
    <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.9);line-height:1.5;margin:0 0 20px 0;">Aprenda a diferenciar a fome do seu corpo da fome da sua mente — e retome o controle.</p>
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

# ---------- SLIDE 2: FOME FÍSICA ----------
slides.append(f'''<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:16px;">SINAL 1</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:{DARK_BG};line-height:1.15;margin:0 0 18px 0;">Fome física: a fome do corpo</h2>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:#4a4a42;line-height:1.6;margin:0 0 18px 0;">É a necessidade biológica real de alimento. Vem de forma gradual, com o passar das horas, e qualquer comida minimamente adequada resolve.</p>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🕐</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Surge gradualmente</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Horas após a última refeição</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🍽️</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Qualquer comida serve</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Não há uma vontade específica e fixa</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">✅</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Satisfaz e para</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Você come e a vontade desaparece</span></div>
    </div>
  </div>
  {swipe_arrow(True)}
</div>''')

# ---------- SLIDE 3: FOME EMOCIONAL ----------
slides.append(f'''<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:16px;">SINAL 2</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 18px 0;">Fome emocional: a fome da mente</h2>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.7);line-height:1.6;margin:0 0 18px 0;">Não nasce da necessidade de energia — nasce de uma emoção. Estresse, ansiedade, tédio, tristeza e até hábito viram vontade de comer.</p>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.08);">
      <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">⚡</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Surge de repente</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Vontade urgente, geralmente de um alimento específico</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.08);">
      <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🍫</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Desejo específico</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">"Só aquilo resolve" — doce, salgado, fast-food</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;">
      <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">😔</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Não satisfaz e gera culpa</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Continua comendo e, depois, vem o peso da culpa</span></div>
    </div>
  </div>
  {swipe_arrow(False)}
</div>''')

# ---------- SLIDE 4: COMPARATIVO ----------
slides.append(f'''<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:center;padding:0 36px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:16px;">COMPARE</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:{DARK_BG};line-height:1.15;margin:0 0 18px 0;">Uma do lado da outra</h2>
  <div style="display:flex;gap:12px;margin-bottom:16px;">
    <div style="flex:1;padding:16px;background:{DARK_BG};border-radius:12px;">
      <span style="font-family:'{FONT_BODY}',sans-serif;font-size:11px;font-weight:700;letter-spacing:1px;color:{BRAND_LIGHT};display:block;margin-bottom:10px;">FÍSICA</span>
      <span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.85);line-height:1.5;display:block;">Começa devagar • qualquer comida serve • para quando sacia • vem de estômago vazio</span>
    </div>
    <div style="flex:1;padding:16px;background:{BRAND_PRIMARY};border-radius:12px;">
      <span style="font-family:'{FONT_BODY}',sans-serif;font-size:11px;font-weight:700;letter-spacing:1px;color:#fff;display:block;margin-bottom:10px;">EMOCIONAL</span>
      <span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.95);line-height:1.5;display:block;">Surge de repente • desejo específico • não para saciado • vem com uma emoção</span>
    </div>
  </div>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:#8A8580;line-height:1.5;margin:0;">A pergunta-chave: <b style="color:{DARK_BG};">"Estou comendo por fome ou por emoção?"</b></p>
  {swipe_arrow(True)}
</div>''')

# ---------- SLIDE 5: ESCALA DA FOME ----------
slides.append(f'''<div class="slide" style="background:linear-gradient(165deg, {BRAND_DARK} 0%, {BRAND_PRIMARY} 55%, {BRAND_LIGHT} 100%);display:flex;flex-direction:column;justify-content:center;padding:0 36px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:rgba(255,255,255,0.8);margin-bottom:16px;">FERRAMENTA PRÁTICA</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:29px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 18px 0;">A escala da fome (1 a 10)</h2>
  <div style="display:flex;flex-direction:column;gap:8px;margin-bottom:18px;">
    <div style="display:flex;align-items:center;gap:12px;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:22px;font-weight:700;color:#fff;min-width:56px;">1–2</span>
      <div style="flex:1;height:10px;background:rgba(255,255,255,0.25);border-radius:6px;"><div style="height:100%;width:20%;background:#fff;border-radius:6px;"></div></div>
      <span style="font-family:'{FONT_BODY}',sans-serif;font-size:11px;color:rgba(255,255,255,0.85);width:120px;text-align:right;">Faminto demais</span>
    </div>
    <div style="display:flex;align-items:center;gap:12px;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:22px;font-weight:700;color:#fff;min-width:56px;">3–4</span>
      <div style="flex:1;height:10px;background:rgba(255,255,255,0.25);border-radius:6px;"><div style="height:100%;width:40%;background:#fff;border-radius:6px;"></div></div>
      <span style="font-family:'{FONT_BODY}',sans-serif;font-size:11px;color:rgba(255,255,255,0.85);width:120px;text-align:right;">Hora de comer 🍽️</span>
    </div>
    <div style="display:flex;align-items:center;gap:12px;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:22px;font-weight:700;color:#fff;min-width:56px;">5</span>
      <div style="flex:1;height:10px;background:rgba(255,255,255,0.25);border-radius:6px;"><div style="height:100%;width:50%;background:#fff;border-radius:6px;"></div></div>
      <span style="font-family:'{FONT_BODY}',sans-serif;font-size:11px;color:rgba(255,255,255,0.85);width:120px;text-align:right;">Nem fome, nem saciedade</span>
    </div>
    <div style="display:flex;align-items:center;gap:12px;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:22px;font-weight:700;color:#fff;min-width:56px;">6–7</span>
      <div style="flex:1;height:10px;background:rgba(255,255,255,0.25);border-radius:6px;"><div style="height:100%;width:70%;background:#fff;border-radius:6px;"></div></div>
      <span style="font-family:'{FONT_BODY}',sans-serif;font-size:11px;color:rgba(255,255,255,0.85);width:120px;text-align:right;">Satisfeito — parar aqui ✅</span>
    </div>
    <div style="display:flex;align-items:center;gap:12px;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:22px;font-weight:700;color:#fff;min-width:56px;">8–10</span>
      <div style="flex:1;height:10px;background:rgba(255,255,255,0.25);border-radius:6px;"><div style="height:100%;width:95%;background:#fff;border-radius:6px;"></div></div>
      <span style="font-family:'{FONT_BODY}',sans-serif;font-size:11px;color:rgba(255,255,255,0.85);width:120px;text-align:right;">Estufado, desconfortável</span>
    </div>
  </div>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:rgba(255,255,255,0.9);line-height:1.5;margin:0;font-weight:600;">Coma entre 3 e 7 — nem faminto demais, nem estufado demais.</p>
  {swipe_arrow(False)}
</div>''')

# ---------- SLIDE 6: GATILHOS EMOCIONAIS ----------
slides.append(f'''<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:16px;">GATILHOS</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 18px 0;">O que aciona a fome emocional?</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.08);">
      <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">😫</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Estresse e ansiedade</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Comer vira válvula de escape e conforto</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.08);">
      <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">😴</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Tédio e hábito</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Comer no sofá, no celular, no meio da noite</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.08);">
      <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🍬</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Restrição excessiva</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Dieta rígida demais → vontade explosiva depois</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;">
      <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🤐</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Emoções não nomeadas</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Tristeza, raiva, solidão — sem espaço para falar</span></div>
    </div>
  </div>
  {swipe_arrow(False)}
</div>''')

# ---------- SLIDE 7: ESTRATÉGIAS PRÁTICAS ----------
slides.append(f'''<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:16px;">PASSO A PASSO</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:{DARK_BG};line-height:1.15;margin:0 0 18px 0;">Estratégias para retomar o controle</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:16px;padding:12px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">01</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Dê uma pausa de 10 minutos</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Se a vontade passar, era emocional</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:16px;padding:12px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">02</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Nomeie a emoção</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Estou estressado? Entediado? Cansado? O que eu preciso de verdade?</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:16px;padding:12px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">03</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Use a escala da fome</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Abaixo de 3, alimente-se; acima de 7, outro cuidado se faz</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:16px;padding:12px 0;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">04</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:{DARK_BG};display:block;">Sem culpa e sem dieta radical</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Comer emocional é humano — o problema é a frequência e a culpa</span></div>
    </div>
  </div>
  {swipe_arrow(True)}
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
  <title>{BRAND_NAME} - Fome Física vs Fome Emocional</title>
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
      <span class="handle">{INSTA_HANDLE}</span> Fome física vs fome emocional: aprenda a diferenciar e retome o controle da sua alimentação sem culpa. 🧠🍽️ #nutricao #fomeemocional #comportamentoalimentar
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

output_dir = BASE_DIR / "slides" / "fome-fisica-vs-fome-emocional"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "carousel.html"
output_path.write_text(html, encoding="utf-8")

legenda = f"""{INSTA_HANDLE}

Fome física vs fome emocional — aprenda a diferenciar e retome o controle

📌 Descrição:
Nem toda fome vem do estômago. A fome emocional nasce das emoções — estresse, ansiedade, tédio, tristeza — e se disfarça de vontade de comer. Neste carrossel, explico as diferenças entre fome física e fome emocional, apresento a escala da fome (1 a 10) como ferramenta prática, os principais gatilhos emocionais e estratégias para comer com mais consciência, sem culpa e sem dieta radical.

📝 Resumo:
• Fome física: surge gradualmente, qualquer comida serve e desaparece quando você está satisfeito
• Fome emocional: surge de repente, tem desejo específico e não acaba nem depois de comer
• A escala da fome (1 a 10) ajuda a comer entre 3 e 7 — nem faminto demais, nem estufado demais
• Gatilhos comuns: estresse, ansiedade, tédio, hábito, restrição excessiva e emoções não nomeadas
• Estratégias: pausa de 10 minutos, nomear a emoção, usar a escala e abandonar a culpa
• Comer emocional é humano — o problema não é a vontade, é a frequência e a culpa que a acompanha

📚 Fontes:
Literatura de Nutrição Comportamental e Mindful Eating
OMS — Organização Mundial da Saúde (guia de alimentação e comportamento)
Estudos sobre Eating Behavior e regulação emocional da alimentação

🏷️ Hashtags:
#nutricao #nutricaocomportamental #fomeemocional #fomefisica #comportamentoalimentar #alimentacaoconsciente #mindfuleating #saude #bemestar #nutricionista #veronicabomfim #recife

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
