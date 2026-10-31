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
TEMA = "ciclo-comer-emocional"
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


img1_path = get_capa_para_tema(TEMA)
profile_data_uri = load_image_base64(img1_path) if img1_path else None

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


topic = "O ciclo do comer emocional"
hook = "Não é falta de força de vontade — é um ciclo. E ciclo tem como sair."

slide1_img = ""
if profile_data_uri:
    slide1_img = f'''<img src="{profile_data_uri}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;">
  <div style="position:absolute;inset:0;background:linear-gradient(to bottom, rgba(0,0,0,0.35) 0%, rgba(0,0,0,0.65) 100%);z-index:1;"></div>'''

slides = []

# ============================================
# SLIDE 1 — CAPA
# ============================================
slides.append(f'''
<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 60px;overflow:hidden;position:relative;">
  {slide1_img}
  <div style="position:relative;z-index:2;">
    <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:16px;">NUTRIÇÃO COMPORTAMENTAL</span>
    <h1 style="font-family:'{FONT_HEADING}',serif;font-size:30px;font-weight:700;color:#fff;line-height:1.08;margin:0 0 14px 0;">{topic}</h1>
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
# SLIDE 2 — O CICLO (5 etapas)
# ============================================
slides.append(f'''
<div class="slide" style="background:linear-gradient(165deg, {BRAND_DARK} 0%, #55664a 55%, {BRAND_PRIMARY} 100%);display:flex;flex-direction:column;justify-content:center;padding:0 32px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:rgba(255,255,255,0.85);margin-bottom:14px;">O CICLO</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:25px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 16px 0;">São 5 etapas — e elas se repetem</h2>
  <div style="display:flex;flex-direction:column;gap:8px;">
    <div style="display:flex;align-items:center;gap:12px;padding:9px 12px;background:rgba(0,0,0,0.28);border-radius:8px;border:1px solid rgba(255,255,255,0.16);">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:17px;color:{BRAND_LIGHT};font-weight:700;min-width:20px;">1</span>
      <div><span style="font-family:'{FONT_HEADING}',serif;font-size:14px;color:#fff;font-weight:600;">Gatilho</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:11px;color:rgba(255,255,255,0.68);display:block;">Briga, prazo, tédio, cobrança — uma situação, não uma fome</span></div>
    </div>
    <div style="display:flex;align-items:center;gap:12px;padding:9px 12px;background:rgba(0,0,0,0.28);border-radius:8px;border:1px solid rgba(255,255,255,0.16);">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:17px;color:{BRAND_LIGHT};font-weight:700;min-width:20px;">2</span>
      <div><span style="font-family:'{FONT_HEADING}',serif;font-size:14px;color:#fff;font-weight:600;">Emoção</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:11px;color:rgba(255,255,255,0.68);display:block;">Ansiedade, tristeza ou raiva tomam conta do momento</span></div>
    </div>
    <div style="display:flex;align-items:center;gap:12px;padding:9px 12px;background:rgba(0,0,0,0.28);border-radius:8px;border:1px solid rgba(255,255,255,0.16);">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:17px;color:{BRAND_LIGHT};font-weight:700;min-width:20px;">3</span>
      <div><span style="font-family:'{FONT_HEADING}',serif;font-size:14px;color:#fff;font-weight:600;">Craving</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:11px;color:rgba(255,255,255,0.68);display:block;">O cérebro pede alívio rápido — e a comida parece a saída</span></div>
    </div>
    <div style="display:flex;align-items:center;gap:12px;padding:9px 12px;background:rgba(0,0,0,0.28);border-radius:8px;border:1px solid rgba(255,255,255,0.16);">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:17px;color:{BRAND_LIGHT};font-weight:700;min-width:20px;">4</span>
      <div><span style="font-family:'{FONT_HEADING}',serif;font-size:14px;color:#fff;font-weight:600;">Comer</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:11px;color:rgba(255,255,255,0.68);display:block;">O alívio chega em minutos — e o cérebro recompensa a escolha</span></div>
    </div>
    <div style="display:flex;align-items:center;gap:12px;padding:9px 12px;background:rgba(191,149,102,0.22);border-radius:8px;border:1px solid rgba(255,255,255,0.28);">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:17px;color:#fff;font-weight:700;min-width:20px;">5</span>
      <div><span style="font-family:'{FONT_HEADING}',serif;font-size:14px;color:#fff;font-weight:600;">Culpa</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:11px;color:rgba(255,255,255,0.75);display:block;">A voz crítica volta — e a ansiedade reinicia o ciclo</span></div>
    </div>
  </div>
  <div style="display:flex;align-items:center;justify-content:center;gap:10px;margin-top:14px;">
    <span style="font-family:'{FONT_BODY}',sans-serif;font-size:11px;color:rgba(255,255,255,0.7);letter-spacing:1px;">↻ VOLTA AO GATILHO</span>
  </div>
  {swipe_arrow(False)}
</div>
''')

# ============================================
# SLIDE 3 — POR QUE O CORPO FAZ ISSO
# ============================================
slides.append(f'''
<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:center;padding:0 34px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:14px;">O QUE ACONTECE NO CORPO</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:24px;font-weight:600;color:#fff;line-height:1.16;margin:0 0 16px 0;">Comer é a forma mais rápida de acalmar o sistema nervoso</h2>
  <div style="display:flex;flex-direction:column;gap:9px;">
    <div style="padding:11px 14px;background:rgba(191,149,102,0.12);border:1px solid rgba(191,149,102,0.3);border-radius:9px;">
      <p style="font-family:'{FONT_BODY}',sans-serif;font-size:10px;color:{BRAND_LIGHT};margin:0 0 3px 0;letter-spacing:1px;">ALÍVIO IMEDIATO</p>
      <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:#fff;margin:0;line-height:1.45;">A sensação de conforto chega antes da solução — e o corpo aprende a repetir.</p>
    </div>
    <div style="padding:11px 14px;background:rgba(191,149,102,0.12);border:1px solid rgba(191,149,102,0.3);border-radius:9px;">
      <p style="font-family:'{FONT_BODY}',sans-serif;font-size:10px;color:{BRAND_LIGHT};margin:0 0 3px 0;letter-spacing:1px;">CULPA QUE VOLTA MAIS FORTE</p>
      <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:#fff;margin:0;line-height:1.45;">O julgamento aumenta a ansiedade — que é exatamente o gatilho do próximo ciclo.</p>
    </div>
    <div style="padding:11px 14px;background:rgba(191,149,102,0.2);border:1px solid rgba(191,149,102,0.42);border-radius:9px;">
      <p style="font-family:'{FONT_BODY}',sans-serif;font-size:10px;color:{BRAND_LIGHT};margin:0 0 3px 0;letter-spacing:1px;">QUEM SE RESTRINGE MAIS PERDE O CONTROLE</p>
      <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:#fff;margin:0;line-height:1.45;">No estudo clássico de Herman &amp; Polivy (1975), quem se restringia comia muito mais quando era liberada a escolher — o "cheese factor".</p>
    </div>
  </div>
  {swipe_arrow(False)}
</div>
''')

# ============================================
# SLIDE 4 — SINAIS DE ALERTA
# ============================================
slides.append(f'''
<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:center;padding:0 36px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:14px;">SINAIS DE ALERTA</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:25px;font-weight:600;color:#1e293b;line-height:1.16;margin:0 0 14px 0;">Sinais de que você está dentro do ciclo</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:14px;padding:9px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">✦</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:13.5px;font-weight:600;color:#1e293b;display:block;">Comer rápido e em segredo</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:11.5px;color:#8A8580;">Você escolhe o que dá menos problemas, não o que dá vontade</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:9px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">✦</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:13.5px;font-weight:600;color:#1e293b;display:block;">Culpa logo depois da refeição</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:11.5px;color:#8A8580;">A comida vira assunto de julgamento, e não de uma refeição</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:9px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">✦</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:13.5px;font-weight:600;color:#1e293b;display:block;">Fome mesmo depois de comer</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:11.5px;color:#8A8580;">O pedido continua porque o alívio não veio de verdade</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:9px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">✦</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:13.5px;font-weight:600;color:#1e293b;display:block;">"Começo na segunda-feira"</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:11.5px;color:#8A8580;">Adiar o recomeço é o que mantém o padrão vivo</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:9px 0;">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">✦</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:13.5px;font-weight:600;color:#1e293b;display:block;">Exercício e jejum como punição</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:11.5px;color:#8A8580;">Transformar a comida em dívida só alimenta o ciclo</span></div>
    </div>
  </div>
  {swipe_arrow(True)}
</div>
''')

# ============================================
# SLIDE 5 — A ARMADILHA DA COMPENSAÇÃO
# ============================================
slides.append(f'''
<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:center;padding:0 34px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:14px;">A ARMADILHA</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:25px;font-weight:600;color:#1e293b;line-height:1.16;margin:0 0 8px 0;">A "compensação" é o que mantém o ciclo vivo</h2>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:12.5px;color:#8A8580;line-height:1.5;margin:0 0 14px 0;">Depois de comer fora do padrão, três pensamentos quase sempre aparecem:</p>
  <div style="display:flex;flex-direction:column;gap:9px;">
    <div style="padding:11px 14px;background:rgba(191,149,102,0.12);border-left:3px solid {BRAND_PRIMARY};border-radius:7px;">
      <p style="font-family:'{FONT_BODY}',sans-serif;font-size:12.5px;color:#1e293b;font-weight:600;margin:0 0 3px 0;">"Já estraguei mesmo — vou comer o que der."</p>
      <p style="font-family:'{FONT_BODY}',sans-serif;font-size:11.5px;color:#8A8580;margin:0;">O excesso de um dia vira excesso de dois dias.</p>
    </div>
    <div style="padding:11px 14px;background:rgba(191,149,102,0.12);border-left:3px solid {BRAND_PRIMARY};border-radius:7px;">
      <p style="font-family:'{FONT_BODY}',sans-serif;font-size:12.5px;color:#1e293b;font-weight:600;margin:0 0 3px 0;">"Vou punir com jejum ou treino pesado."</p>
      <p style="font-family:'{FONT_BODY}',sans-serif;font-size:11.5px;color:#8A8580;margin:0;">A restrição volta — e com ela, mais craving.</p>
    </div>
    <div style="padding:11px 14px;background:rgba(191,149,102,0.12);border-left:3px solid {BRAND_PRIMARY};border-radius:7px;">
      <p style="font-family:'{FONT_BODY}',sans-serif;font-size:12.5px;color:#1e293b;font-weight:600;margin:0 0 3px 0;">"A partir de amanhã eu faço direitinho."</p>
      <p style="font-family:'{FONT_BODY}',sans-serif;font-size:11.5px;color:#8A8580;margin:0;">Adiar a mudança mantém o gatilho ativo.</p>
    </div>
  </div>
  <div style="margin-top:14px;padding:12px 14px;background:{BRAND_DARK};border-radius:8px;">
    <p style="font-family:'{FONT_HEADING}',serif;font-size:13.5px;color:#fff;font-style:italic;line-height:1.4;margin:0;">A punição não corrige a refeição — ela prepara a próxima.</p>
  </div>
  {swipe_arrow(True)}
</div>
''')

# ============================================
# SLIDE 6 — COMO QUEBRAR O CICLO
# ============================================
slides.append(f'''
<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:center;padding:0 34px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:14px;">O QUE FAZER</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:25px;font-weight:600;color:#fff;line-height:1.16;margin:0 0 16px 0;">5 passos para sair do ciclo</h2>
  <div style="display:flex;flex-direction:column;gap:8px;">
    <div style="display:flex;align-items:flex-start;gap:14px;padding:9px 12px;background:rgba(191,149,102,0.12);border:1px solid rgba(191,149,102,0.3);border-radius:9px;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:17px;color:{BRAND_PRIMARY};font-weight:700;min-width:26px;">01</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:13.5px;color:#fff;font-weight:600;display:block;">Pause 10 minutos antes de comer</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:11.5px;color:rgba(255,255,255,0.6);">Entre o gatilho e o primeiro biscoito cabe uma pausa</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:9px 12px;background:rgba(191,149,102,0.12);border:1px solid rgba(191,149,102,0.3);border-radius:9px;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:17px;color:{BRAND_PRIMARY};font-weight:700;min-width:26px;">02</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:13.5px;color:#fff;font-weight:600;display:block;">Nomeie a emoção</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:11.5px;color:rgba(255,255,255,0.6);">Pergunte: o que eu preciso agora — descanso, conversa ou ajuda?</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:9px 12px;background:rgba(191,149,102,0.12);border:1px solid rgba(191,149,102,0.3);border-radius:9px;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:17px;color:{BRAND_PRIMARY};font-weight:700;min-width:26px;">03</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:13.5px;color:#fff;font-weight:600;display:block;">Coma sem punir</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:11.5px;color:rgba(255,255,255,0.6);">Mesa, sem tela e sem balanço de calorias depois</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:9px 12px;background:rgba(191,149,102,0.12);border:1px solid rgba(191,149,102,0.3);border-radius:9px;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:17px;color:{BRAND_PRIMARY};font-weight:700;min-width:26px;">04</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:13.5px;color:#fff;font-weight:600;display:block;">Regule os horários das refeições</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:11.5px;color:rgba(255,255,255,0.6);">Pular refeições intensifica o craving da tarde</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:9px 12px;background:rgba(191,149,102,0.2);border:1px solid rgba(191,149,102,0.42);border-radius:9px;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:17px;color:{BRAND_PRIMARY};font-weight:700;min-width:26px;">05</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:13.5px;color:#fff;font-weight:600;display:block;">Busque apoio profissional</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:11.5px;color:rgba(255,255,255,0.65);">Se o ciclo atrapalha sua rotina e seu humor, não é força de vontade que falta</span></div>
    </div>
  </div>
  {swipe_arrow(False)}
</div>
''')

# ============================================
# SLIDE 7 — FECHAMENTO
# ============================================
slides.append(f'''
<div class="slide" style="background:linear-gradient(165deg, {BRAND_DARK} 0%, #5a6b4f 60%, {BRAND_PRIMARY} 100%);display:flex;flex-direction:column;justify-content:center;padding:0 36px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:rgba(255,255,255,0.85);margin-bottom:16px;">A MENSAGEM FINAL</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#fff;line-height:1.14;margin:0 0 16px 0;">Comer emocional não é fracasso moral</h2>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.85);line-height:1.55;margin:0 0 20px 0;">É um ciclo de alívio e compensação. Ciclos não se resolvem com cobrança — se interrompem com estratégia.</p>
  <div style="padding:16px 18px;background:rgba(0,0,0,0.28);border-left:3px solid {BRAND_LIGHT};border-radius:6px;">
    <p style="font-family:'{FONT_HEADING}',serif;font-size:15px;color:#fff;font-style:italic;line-height:1.45;margin:0;">"Você não quebrou o ciclo pela força de vontade. Quebrou porque encontrou um jeito melhor de lidar com a emoção."</p>
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
      <span class="handle">{INSTA_HANDLE}</span> {hook} Entenda as 5 etapas do ciclo, os sinais de alerta e o que fazer para interromper. #comeraemocional #nutricaocomportamental #alimentacaoconsciente
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

output_file = str(BASE_DIR / "slides" / TEMA / "carousel.html")
slides_dir = Path(output_file).parent
slides_dir.mkdir(exist_ok=True)
Path(output_file).write_text(html, encoding="utf-8")

legenda = f"""{INSTA_HANDLE}

O ciclo do comer emocional: como funciona e como sair dele

📌 Descrição:
Você come por motivo emocional e depois se sente culpada — e o ciclo recomeça mais forte. O comer emocional não é falta de força de vontade: é um mecanismo de alívio que o cérebro aprende e repete. Neste carrossel, mostro as 5 etapas do ciclo (gatilho, emoção, craving, comer e culpa), por que a "compensação" depois de comer fora do padrão é o que o mantém vivo, os sinais de alerta e cinco estratégias práticas para interromper o ciclo no dia a dia.

📝 Resumo:
• O ciclo tem 5 etapas: gatilho → emoção → craving → comer → culpa, e a culpa reinicia o ciclo
• Comer é a forma mais rápida de acalmar o sistema nervoso — o alívio vem antes da solução
• No estudo clássico de Herman & Polivy (1975), quem se restringe acaba comendo mais quando é liberado ("cheese factor")
• Sinais de alerta: comer rápido e em segredo, culpa após a refeição, fome mesmo depois de comer, "começo na segunda" e exercício punitivo
• A "compensação" (jejum, treino punitivo, recomeçar depois) prepara o próximo episódio de perda de controle
• Para sair: pausar 10 minutos, nomear a emoção, comer sem punição, manter horários regulares e buscar apoio profissional

📚 Fontes:
Herman, C. P. & Polivy, J. (1975) — Eating in the absence of hunger ("cheese factor")
Cochrane, K. H. & Herman, C. P. — Restraint, eating and mood
Literatura de Nutrição Comportamental e Comportamento Alimentar
Instituto Nacional de Câncer (INCA) — alimentação e bem-estar emocional
Guia Alimentar para a População Brasileira — Ministério da Saúde (OMS/OPAS)

🏷️ Hashtags:
#comeraemocional #ciclocomeraemocional #nutricaocomportamental #comportamentoalimentar #reeducacaalimentar #saudemental #alimentacaoconsciente #intuitiveeating #nutricao #nutricionista #veronicabomfim #recife

📞 Contato:
📱 {CONTACT_PHONE}
📧 {CONTACT_EMAIL}
📸 {INSTA_HANDLE}
🌐 {CONTACT_WEBSITE}
"""

slides_dir.joinpath("legenda.txt").write_text(legenda, encoding="utf-8")

print(f"Capa utilizada: {img1_path}")
print(f"Carrossel criado: {output_file}")
print(f"Legenda criada: {slides_dir / 'legenda.txt'}")
print(f"Total de slides: {TOTAL_SLIDES}")