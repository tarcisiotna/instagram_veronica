# Brand Identity: Verônica Bomfim de Lima

## Default Brand Details (use when user doesn't specify)

- **Brand name**: Verônica Bomfim de Lima
- **Instagram handle**: @veronicabomfim.nutri
- **Primary brand color**: #bf9566 (gold/brown from project brand guide)
- **Logo**: Use first letter "V" or profile photo
- **Font preference**: Playfair Display (heading) + TT Norms (body) — per project brand guide
- **Tone**: Professional yet warm, trustworthy, health-focused
- **Idioma**: Português (BR)
- **Carousel format**: Standard (7 slides)

## Contact Information (add to CTA slide)

- **Phone**: (81) 9 9864-5846
- **Email**: veronicabomfim.nutri@gmail.com
- **Instagram**: @veronicabomfim.nutri

## Profile Images

Available in: `/home/tarcisio/instagram_veronica/Imagens/nanobanana/`

**Rule Slide 1**: Use a RANDOM photo from this folder each time a new carousel is created.

## Slide 1 Image Rule (NEW RULE)

**Always use a RANDOM photo from**: `/home/tarcisio/instagram_veronica/Imagens/nanobanana/`

- Each time a new carousel is created, pick a random `.jpeg` image from the nanobanana folder
- This ensures variety and avoids repeating the same photo on Slide 1
- Use Python's `random.choice()` to pick a random image from the folder

## Final Slide Image (NEW RULE)

**Always use**: `/home/tarcisio/instagram_veronica/Imagens/CTA/CTA.png`

- This image must be placed as a background in the CTA slide (Slide 7)
- Position: absolute, inset: 0
- Object-fit: cover
- Z-index: 0
- **Rule**: Never use any other image for the CTA slide — always use CTA.png
- The image already contains all contact information (no additional text needed)

## Research Sources (ALWAYS consult before creating content)

When creating ANY carousel for Verônica Bomfim de Lima, ALWAYS research first at:

1. **INCA (Instituto Nacional de Câncer)** - https://www.gov.br/inca/pt-br
   - Use for: cancer prevention, healthy eating, nutrition guidelines, official health data
   - Search for: "alimentação saudável", "prevenção de câncer", "nutrição"

2. **SBNO (Sociedade Brasileira de Nutrição Oncológica)** - https://sbno.com.br/
   - Use for: oncology nutrition, specialized diets, clinical nutrition guidelines
   - Search for: "nutrição oncológica", "dietas especiais", "evidências científicas"

**Rule**: Always cite INCA or SBNO as sources when using their data or guidelines in slides.

## Color Palette (from project brand guide Documento/Guia da marca.md)

- BRAND_PRIMARY: #bf9566 (gold/brown)
- BRAND_LIGHT: #ecd7ba (light cream)
- BRAND_DARK: #394233 (dark slate)
- LIGHT_BG: #FAF9F7 (warm off-white)
- LIGHT_BORDER: #ecd7ba (light cream)
- DARK_BG: #394233 (dark slate)

## Typography (from project brand guide)

- **Headings**: Playfair Display
- **Body**: TT Norms
- **Support**: Evolve Sans / Nesans

## CTA Slide Default Text

**Note**: Slide 7 uses only CTA.png background image (no additional text)

**Contact footer** (for reference):
- (81) 9 9864-5846
- veronicabomfim.nutri@gmail.com
- @veronicabomfim.nutri

## Arquivo legendas.txt (Padrão Obrigatório)

Todo carrossel deve ter um arquivo `legendas.txt` (ou `legenda.txt` se já existir) com o seguinte padrão:

```
📷 @veronicabomfim.nutri

[Título do carrossel]

📌 Descrição:
[Texto de descrição explicando o tema]

📝 Resumo:
• Item 1
• Item 2
• Item 3

📚 Fontes:
INCA — [nome da fonte]
SBNO — [nome da fonte]

🏷️ Hashtags:
#hashtag1 #hashtag2 #hashtag3

📞 Contato:
📱 (81) 9 9864-5846
📧 veronicabomfim.nutri@gmail.com
📷 @veronicabomfim.nutri
🌐 https://veronicabomfimnutriweb.pages.dev/
```

**Regras:**
- Usar emojis para cada seção (📷, 📌, 📝, 📚, 🏷️, 📞)
- Sem acentos nos emojis ou texto (evitar erros de codificação)
- Sempre incluir contatos no final
- Salvar na mesma pasta do carrossel: `slides/[assunto]/legendas.txt`
