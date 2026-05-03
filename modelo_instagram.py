import base64
from pathlib import Path
import sys

# ============================================
# VALIDAÇÃO DAS REGRAS - NÃO VIOLAR!
# ============================================
# Verificar se está usando imagens de alta qualidade
for img_path in [
    "/home/tarcisio/instagram_veronica/Imagens/foto1.jpeg",
]:
    if Path(img_path).exists():
        size_mb = Path(img_path).stat().st_size / 1024 / 1024
        if size_mb < 1:
            print(f"⚠️  REGRA VIOLADA: {img_path} tem apenas {size_mb:.1f}MB!")
            print("   Use apenas imagens >7MB: 0AVA3114.jpg, 0AVA3115.jpg, etc.")
            sys.exit(1)

# ============================================
# REGRA PADRÃO PARA TODOS OS CARROSSÉIS
# ============================================
# 1. Slide 7 (CTA): Usar logotipo sem fundo da pasta "Imagens/Sem fundo/"
# 2. Slide 7: Textos em branco (#fff) com sombras para melhor legibilidade
# 3. Slide 7: Remover divisor branco (divider) e overlay
# 4. Slide 7: Remover barra de progresso (slides finais não têm)
# 5. Slide 7: Fontes maiores (18px nome, 15px contatos, 15px botão)
# 6. Cores seguindo Guia da marca.md: #bf9566 (bronze), #ecd7ba, #FAF9F7, #394233
# 7. Tipografia: Playfair Display (títulos) + TT Norms (textos)
# 8. Legenda: Gerar slides/legenda.txt com descrição, resumo, fontes, hashtags, contato
# 9. Slides exportados: usar device_scale_factor (420px → 1080px)
# 10. Nunca usar "Dica da especialista" - usar apenas "Dica"
# 11. Slide 7: Usar apenas "Agende sua consulta" - nunca "com a especialista"
# 12. Slide 1: Usar logotipo sem fundo da pasta "Imagens/Sem fundo/" (igual ao Slide 7)
# ============================================

# Brand: Verônica Bomfim de Lima - seguindo Guia da marca.md
BRAND_PRIMARY = "#bf9566"  # Bronze (cor principal)
BRAND_LIGHT = "#ecd7ba"    # Bege claro
BRAND_DARK = "#394233"     # Verde escuro/charcoal
LIGHT_BG = "#FAF9F7"      # Off-white (quase branco)
LIGHT_BORDER = "#ecd7ba"  # Bege claro para bordas
DARK_BG = "#394233"        # Fundo escuro
FONT_HEADING = "Playfair Display"
FONT_BODY = "TT Norms"
BRAND_NAME = "Verônica Bomfim de Lima"
INSTA_HANDLE = "@veronicabomfim.nutri"
TOTAL_SLIDES = 7
CONTACT_PHONE = "(81) 9 9864-5846"
CONTACT_EMAIL = "veronicabomfim.nutri@gmail.com"

# Profile images for Slide 1 - USAR SEMPRE AS MAIORES PRIMEIRO
PROFILE_IMAGES = [
    "/home/tarcisio/instagram_veronica/Imagens/0AVA3114.jpg",
    "/home/tarcisio/instagram_veronica/Imagens/0AVA3115.jpg",
    "/home/tarcisio/instagram_veronica/Imagens/0AVA3120.jpg",
    "/home/tarcisio/instagram_veronica/Imagens/0AVA3125.jpg",
    "/home/tarcisio/instagram_veronica/Imagens/0AVA3129.jpg",
    "/home/tarcisio/instagram_veronica/Imagens/0AVA3131.jpg",
]

# Logo images (without background) for Slide 7
LOGO_IMAGES = [
    "/home/tarcisio/instagram_veronica/Imagens/Sem fundo/1.png",
    "/home/tarcisio/instagram_veronica/Imagens/Sem fundo/2.png",
    "/home/tarcisio/instagram_veronica/Imagens/Sem fundo/3.png",
    "/home/tarcisio/instagram_veronica/Imagens/Sem fundo/4.png",
    "/home/tarcisio/instagram_veronica/Imagens/Sem fundo/5.png",
    "/home/tarcisio/instagram_veronica/Imagens/Sem fundo/6.png",
    "/home/tarcisio/instagram_veronica/Imagens/Sem fundo/7.png",
    "/home/tarcisio/instagram_veronica/Imagens/Sem fundo/8.png",
    "/home/tarcisio/instagram_veronica/Imagens/Sem fundo/9.png",
]

# Rotate image for Slide 1
state_file = Path("/home/tarcisio/instagram_veronica/.opencode/skills/instagram-carousel/last_image.txt")
if state_file.exists():
    last_idx = int(state_file.read_text().strip())
    next_idx = (last_idx + 1) % len(PROFILE_IMAGES)
else:
    next_idx = 0
state_file.write_text(str(next_idx))
profile_img_path = PROFILE_IMAGES[next_idx]

# Load image as base64
def load_image_base64(image_path):
    path = Path(image_path)
    if not path.exists():
        return None
    mime = "image/jpeg"
    if path.suffix.lower() == ".png":
        mime = "image/png"
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"

profile_data_uri = load_image_base64(profile_img_path)
# Use first logo image (or rotate if you want)
logo_data_uri = load_image_base64(LOGO_IMAGES[0])  # Using 1.png as logo

# Progress bar
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

# Swipe arrow
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

# Get topic from command line or use default
topic = sys.argv[1] if len(sys.argv) > 1 else "Reeducação alimentar passo a passo"
hook = sys.argv[2] if len(sys.argv) > 2 else "7 passos para transformar sua relação com a comida"

# Slide 1 - Hook with profile image background
slide1_img = ""
if profile_data_uri:
    slide1_img = f'''<img src="{profile_data_uri}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;">
  <div style="position:absolute;inset:0;background:linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.6) 100%);z-index:1;"></div>'''

slides = []

slides.append(f'''
<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:center;padding:0 36px;overflow:hidden;position:relative;">
  {slide1_img}
  <div style="position:relative;z-index:2;">
    <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:#fff;margin-bottom:16px;">REEDUCAÇÃO ALIMENTAR</span>
    <h1 style="font-family:'{FONT_HEADING}',serif;font-size:32px;font-weight:700;color:#fff;line-height:1.1;margin:0 0 16px 0;">{hook}</h1>
    <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.9);line-height:1.5;margin:0 0 24px 0;">Guia prático baseado no Ministério da Saúde</p>
    <div style="display:flex;align-items:center;gap:12px;margin-top:8px;">
      <div style="width:40px;height:40px;border-radius:50%;background:{BRAND_PRIMARY};display:flex;align-items:center;justify-content:center;color:#fff;font-size:18px;font-weight:700;">V</div>
      <div>
        <span style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;font-weight:600;color:#fff;display:block;letter-spacing:0.5px;">{BRAND_NAME}</span>
        <span style="font-family:'{FONT_BODY}',sans-serif;font-size:11px;color:rgba(255,255,255,0.7);">{INSTA_HANDLE}</span>
      </div>
    </div>
  </div>
  {progress_bar(0, TOTAL_SLIDES, False)}
  {swipe_arrow(False)}
</div>
''')

# Slide 2 - Problem (Myths)
slides.append(f'''
<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:16px;">MITOS COMUNS</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 14px 0;">O que você ouviu não é verdade</h2>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;color:rgba(255,255,255,0.6);line-height:1.5;margin:0 0 12px 0;">Muitos pacientes acreditam que dietas restritivas são o único caminho.</p>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px;">
    <span style="font-size:11px;padding:5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:#94a3b8;text-decoration:line-through;">Dieta restritiva funciona</span>
    <span style="font-size:11px;padding:5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:#94a3b8;text-decoration:line-through;">Preciso cortar carboidratos</span>
  </div>
  {progress_bar(1, TOTAL_SLIDES, False)}
  {swipe_arrow(False)}
</div>
''')

# Slide 3 - Solution (Truths)
slides.append(f'''
<div class="slide" style="background:linear-gradient(165deg, {BRAND_DARK} 0%, {BRAND_PRIMARY} 50%, {BRAND_LIGHT} 100%);display:flex;flex-direction:column;justify-content:center;padding:0 36px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:rgba(255,255,255,0.8);margin-bottom:16px;">A VERDADE</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:30px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 20px 0;">Pequenas mudanças, grandes resultados</h2>
  <div style="padding:20px;background:rgba(0,0,0,0.25);border-radius:12px;border:1px solid rgba(255,255,255,0.15);margin-bottom:16px;">
    <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:rgba(255,255,255,0.7);margin:0 0 8px 0;">Dica</p>
    <p style="font-family:'{FONT_HEADING}',serif;font-size:16px;color:#fff;font-style:italic;line-height:1.5;margin:0;">"Pequenas mudanças diárias geram resultados sustentáveis"</p>
  </div>
  <p style="font-family:'{FONT_BODY}',sans-serif;font-size:13px;color:rgba(255,255,255,0.8);line-height:1.5;margin:0;font-weight:600;">Guia Alimentar + acompanhamento = transformação real.</p>
  {progress_bar(2, TOTAL_SLIDES, False)}
  {swipe_arrow(False)}
</div>
''')

# Slide 4 - Features (Benefits)
slides.append(f'''
<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:16px;">BENEFÍCIOS REAIS</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#1e293b;line-height:1.15;margin:0 0 18px 0;">O que você conquista</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">✦</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#1e293b;display:block;">Saciedade real</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Sem fome constante</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">✦</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#1e293b;display:block;">Mais energia</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Disposição no dia a dia</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;">
      <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;flex-shrink:0;">✦</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#1e293b;display:block;">Relação saudável</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Prazer em comer bem</span></div>
    </div>
  </div>
  {progress_bar(3, TOTAL_SLIDES, True)}
  {swipe_arrow(True)}
</div>
''')

# Slide 5 - Details (Safety)
slides.append(f'''
<div class="slide" style="background:{DARK_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_LIGHT};margin-bottom:16px;">PRINCÍPIOS</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#fff;line-height:1.15;margin:0 0 14px 0;">Pilares da reeducação</h2>
  <div style="display:flex;flex-direction:column;gap:10px;">
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.08);">
      <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🥗</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Comer com prazer</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Sem culpa ou restrição</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.08);">
      <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">⏰</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Regularidade</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Horários consistentes</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;">
      <span style="color:{BRAND_LIGHT};font-size:15px;width:18px;text-align:center;flex-shrink:0;">🩺</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#fff;display:block;">Acompanhamento</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:rgba(255,255,255,0.5);">Nutricionista é essencial</span></div>
    </div>
  </div>
  {progress_bar(4, TOTAL_SLIDES, False)}
  {swipe_arrow(False)}
</div>
''')

# Slide 6 - How-to (Process)
slides.append(f'''
<div class="slide" style="background:{LIGHT_BG};display:flex;flex-direction:column;justify-content:flex-end;padding:0 36px 52px;overflow:hidden;">
  <span style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{BRAND_PRIMARY};margin-bottom:16px;">PASSO A PASSO</span>
  <h2 style="font-family:'{FONT_HEADING}',serif;font-size:28px;font-weight:600;color:#1e293b;line-height:1.15;margin:0 0 18px 0;">3 etapas para começar</h2>
  <div style="display:flex;flex-direction:column;gap:0;">
    <div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">01</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#1e293b;display:block;">Avaliação nutricional</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Entenda seus hábitos atuais</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;border-bottom:1px solid {LIGHT_BORDER};">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">02</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#1e293b;display:block;">Plano personalizado</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Pequenas mudanças graduais</span></div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;">
      <span style="font-family:'{FONT_HEADING}',serif;font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;flex-shrink:0;">03</span>
      <div><span style="font-family:'{FONT_BODY}',sans-serif;font-size:14px;font-weight:600;color:#1e293b;display:block;">Acompanhamento contínuo</span><span style="font-family:'{FONT_BODY}',sans-serif;font-size:12px;color:#8A8580;">Ajustes conforme evolução</span></div>
    </div>
  </div>
  {progress_bar(5, TOTAL_SLIDES, True)}
  {swipe_arrow(True)}
</div>
''')

# Slide 7 - CTA with contact info and final image
final_img_path = "/home/tarcisio/instagram_veronica/Imagens/slide_final.png"
final_img_data_uri = None
if Path(final_img_path).exists():
    mime = "image/jpeg"
    if Path(final_img_path).suffix.lower() == ".png":
        mime = "image/png"
    b64 = base64.b64encode(Path(final_img_path).read_bytes()).decode()
    final_img_data_uri = f"data:{mime};base64,{b64}"

final_bg = f'<img src="{final_img_data_uri}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;">' if final_img_data_uri else f'<div style="position:absolute;inset:0;background:linear-gradient(165deg, {BRAND_DARK} 0%, {BRAND_PRIMARY} 50%, {BRAND_LIGHT} 100%);z-index:0;"></div>'
final_overlay = ''  # Removido para slide 7 - deixar imagem final limpa

# Logo image (without background) - with enhanced visual effects
logo_img_tag = f'<img src="{logo_data_uri}" style="width:140px;height:auto;margin:0 auto 28px;filter:drop-shadow(0 6px 20px rgba(191,149,102,0.5));">' if logo_data_uri else f'<div style="width:80px;height:80px;border-radius:50%;background:{BRAND_PRIMARY};display:flex;align-items:center;justify-content:center;color:#fff;font-size:36px;font-weight:700;margin:0 auto 28px;box-shadow:0 6px 24px rgba(191,149,102,0.5);border:3px solid rgba(255,255,255,0.3);">V</div>'

slides.append(f'''
<div class="slide" style="display:flex;flex-direction:column;justify-content:center;align-items:center;padding:0 36px;overflow:hidden;position:relative;">
  {final_bg}
  {final_overlay}
  <div style="position:relative;z-index:2;text-align:center;width:100%;">
    <!-- Bronze accent bar -->
    <div style="width:60px;height:4px;background:{BRAND_PRIMARY};margin:0 auto 16px;border-radius:2px;"></div>
    
    <!-- Logo (without background) -->
    {logo_img_tag}
    
    <!-- Headline -->
    <h2 style="font-family:'{FONT_HEADING}',serif;font-size:34px;font-weight:600;color:#fff;line-height:1.2;margin:0 0 12px 0;">Pronto para cuidar da sua saúde?</h2>
    
    <!-- Subtitle (centered, larger font) -->
    <p style="font-family:'{FONT_BODY}',sans-serif;font-size:19px;font-weight:500;color:rgba(255,255,255,0.95);line-height:1.5;margin:0 0 28px 0;max-width:340px;text-align:center;">Agenda sua consulta</p>
    
    <!-- CTA Button (larger font) -->
    <div style="display:inline-flex;align-items:center;gap:10px;padding:16px 36px;background:{BRAND_PRIMARY};color:#fff;font-family:'{FONT_BODY}',sans-serif;font-weight:700;font-size:16px;border-radius:28px;cursor:pointer;box-shadow:0 4px 16px rgba(191,149,102,0.3);margin-bottom:20px;">Agendar agora</div>
    
    <!-- Contact Info (white text with shadow for better visibility) -->
    <div style="margin-bottom:6px;">
      <span style="font-family:'{FONT_BODY}',sans-serif;font-size:18px;font-weight:700;color:#fff;letter-spacing:0.3px;text-shadow:0 2px 8px rgba(0,0,0,0.6);">{BRAND_NAME}</span>
    </div>
    <div style="margin-bottom:8px;display:flex;align-items:center;gap:8px;justify-content:center;">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 2px 4px rgba(0,0,0,0.5));"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4.05 0 0 1 15.23 13 4 4 0 0 1 12 14a4 4 0 0 1-3.23-1 4 4 0 0 1-1.78-2.63 4 4 0 0 1 .77-3.23 4 4 0 0 1 2.46-.98 4 4 0 0 1 3.23 1 4 4 0 0 1 .98 2.46 4 4 0 0 1-1.77 3.23z"/></svg>
      <span style="font-family:'{FONT_BODY}',sans-serif;font-size:15px;color:#fff;text-shadow:0 2px 6px rgba(0,0,0,0.5);">{INSTA_HANDLE}</span>
    </div>
    
    <!-- Contact Details (official icons) -->
    <div style="font-size:15px;color:#fff;font-family:'{FONT_BODY}',sans-serif;line-height:1.8;font-weight:500;text-shadow:0 2px 6px rgba(0,0,0,0.5);display:flex;flex-direction:column;gap:6px;align-items:center;">
      <div style="display:flex;align-items:center;gap:8px;">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 2px 4px rgba(0,0,0,0.5));"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-1.5 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-1.5-8.63A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.91.36 1.81.72 2.74a21.94 21.94 0 0 0 .73 6.56 21.72 21.72 0 0 0 6.56.73c.93.36 1.83.59 2.74.72A2 2 0 0 1 22 16.92z"/></svg>
        <span>{CONTACT_PHONE}</span>
      </div>
      <div style="display:flex;align-items:center;gap:8px;">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 2px 4px rgba(0,0,0,0.5));"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
        <span>{CONTACT_EMAIL}</span>
      </div>
    </div>
  </div>
</div>
''')

# Build HTML
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
      <span class="handle">{INSTA_HANDLE}</span> {hook} 🥗 Saúde começa no prato! #nutrição #saudável #dicas
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

output_file = "/home/tarcisio/instagram_veronica/slides/reeducacao-alimentar/carousel.html"
Path(output_file).write_text(html, encoding="utf-8")

# Criar pasta slides se não existir
slides_dir = Path("/home/tarcisio/instagram_veronica/slides")
slides_dir.mkdir(exist_ok=True)

# Gerar arquivo de legenda para Instagram (salvo na pasta slides)
legenda = f"""{INSTA_HANDLE}

{hook}

📌 Descrição:
Canetas emagrecedoras têm revolucionado o tratamento da obesidade. Porém, seu uso exige acompanhamento profissional especializado e não substitui hábitos saudáveis de alimentação.

📝 Resumo:
• Canetas são ferramentas, não milagres isolados - exigem prescrição médica
• Benefícios reais: controle do apetite, saciedade prolongada e auxílio na manutenção do peso
• Segurança: uso apenas com prescrição médica, acompanhamento nutricional e alimentação equilibrada
• 3 etapas: consulta médica para avaliação, acompanhamento nutricional com plano alimentar, monitoramento contínuo

📚 Fontes:
SBNO - Sociedade Brasileira de Nutrição Oncológica
Ministério da Saúde - ANS

🏷️ Hashtags:
#canetasemagrecedoras #obesidade #saudável #dicas #veronicabomfim #nutricionista #saude #bemestar #emagrecimento #acompanhamentonutricional #medicacaoinjetavel

📞 Contato:
📱 {CONTACT_PHONE}
📧 {CONTACT_EMAIL}
{INSTA_HANDLE}"""

slides_dir.joinpath("legenda.txt").write_text(legenda, encoding="utf-8")

print(f"Carrossel criado: {output_file}")
print(f"Legenda criada: /home/tarcisio/instagram_veronica/slides/legenda.txt")
print(f"Imagem de perfil utilizada: {profile_img_path}")
