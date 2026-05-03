# REGRAS PADRÃO - Criação de Carrosséis Instagram

## 📋 REGRAS QUE NÃO PODEM SER VIOLADAS

### 1. 🎨 GERAÇÃO DO HTML
- **SCRIPT**: Usar APENAS `modelo_instagram.py` (baseado em `create_veronica_carousel.py`)
- **NOME DO ARQUIVO**: Gerar SEMPRE como `carousel.html` (nunca `carousel_veronica.html`)
- **DIMENSÕES**: Manter HTML em 420px de largura (export scale para 1080px)
- **IMAGENS**: Excluir `foto1.jpeg` da lista de profile images (só usar imagens >7MB)

### 2. 📸 EXPORT DOS SLIDES  
- **SCRIPT**: Usar APENAS `export_veronica_node.js` (scale factor 2.5714)
- **NOMENCLATURA**: `slide_1.png`, `slide_2.png`... (com UNDERSCORE, não hífen)
- **QUALIDADE**: deviceScaleFactor = 2.5714 (1080/420 = 2.5714x)
- **PASTA**: Salvar na pasta específica do tema (ex: `slides/reeducacao-alimentar/`)

### 3. 📏 DIMENSÕES FINAIS
- **RESOLUÇÃO**: 1080x1350px (proporção 4:5 do Instagram)
- **TAMANHO MÍNIMO**: Slide 1 deve ter ≈1.7-1.8MB (HTML ≈20MB)
- **VERIFICAÇÃO**: Sempre checar `file slide_1.png` = "PNG image data, 1080 x 1350"

### 4. 🖼️ IMAGENS DE PERFIL
- **QUALIDADE**: Usar APENAS imagens >7MB da pasta `Imagens/`
- **EXCLUIR**: Nunca usar `foto1.jpeg` (apenas 81KB)
- **LISTA PERMITIDA**: 
  - `0AVA3114.jpg` (7.1MB)
  - `0AVA3115.jpg` (7.2MB) 
  - `0AVA3120.jpg` (9.8MB)
  - `0AVA3125.jpg` (12.9MB)
  - `0AVA3129.jpg` (12.3MB)
  - `0AVA3131.jpg` (10.9MB)

### 5. 📁 ESTRUTURA DE PASTAS
```
instagram_veronica/
├── slides/
│   ├── canetas-emagrecedoras/    # Referência (funcionou)
│   │   ├── carousel.html         # 20MB
│   │   ├── slide_1.png           # 1.8MB
│   │   └── ...
│   └── NOME-DO-TEMA/            # Novo carrossel
│       ├── carousel.html        # ≈18-21MB
│       ├── slide_1.png          # ≈1.7-1.8MB
│       └── legenda.txt
```

### 6. ⚠️ VERIFICAÇÕES OBRIGATÓRIAS
1. ✅ HTML > 18MB (imagens embedadas em alta qualidade)
2. ✅ Slide 1 > 1.7MB (alta resolução)
3. ✅ Dimensões 1080x1350px
4. ✅ Nomes com underscore (`slide_1.png`)
5. ✅ Pasta correta do tema

### 7. 🔄 PROCESSO CORRETO
```bash
# 1. Gerar HTML
python3 modelo_instagram.py "Título" "Subtítulo"

# 2. Exportar slides  
node export_veronica_node.js

# 3. Verificar qualidade
ls -lh slides/NOME-DO-TEMA/slide_1.png
file slides/NOME-DO-TEMA/slide_1.png
```

**VIOLAÇÃO DESTAS REGRAS = SLIDES NÃO FUNCIONAM NO INSTAGRAM**