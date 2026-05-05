# REGRAS PADRÃO - Criação de Carrosséis Instagram

## 📋 REGRAS QUE NÃO PODEM SER VIOLADAS

### 1. 🎨 GERAÇÃO DO HTML
- **SCRIPT**: Usar APENAS `modelo_instagram.py` (baseado em `create_veronica_carousel.py`)
- **NOME DO ARQUIVO**: Gerar SEMPRE como `carousel.html` (nunca `carousel_veronica.html`)
- **DIMENSÕES**: Manter HTML em 420px de largura (export scale para 1080px)
- **IMAGENS**: Usar pasta `Imagens/nanobanana/` (prioritária)

### 2. 📸 EXPORT DOS SLIDES  
- **SCRIPT**: Usar APENAS `export_veronica_node.js` (scale factor 2.5714)
- **NOMENCLATURA**: `slide_1.png`, `slide_2.png`... (com UNDERSCORE, não hífen)
- **QUALIDADE**: deviceScaleFactor = 2.5714 (1080/420 = 2.5714x)
- **PASTA**: Salvar na pasta específica do tema (ex: `slides/reeducacao-alimentar/`)

### 3. 📏 DIMENSÕES FINAIS
- **RESOLUÇÃO**: 1080x1350px (proporção 4:5 do Instagram)
- **TAMANHO MÍNIMO**: HTML >3MB (imagens nanobanana são menores)
- **VERIFICAÇÃO**: Sempre checar `file slide_1.png` = "PNG image data, 1080 x 1350"

### 4. 🖼️ IMAGENS DE PERFIL
- **PRIORIDADE**: Usar pasta `Imagens/nanobanana/` (tamanho menor ~80KB por imagem)
- **QUALIDADE**: Imagens embedadas em alta qualidade no HTML
- **TAMANHO MÍNIMO HTML**: 2.5MB (para garantir qualidade suficiente)

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
1. ✅ HTML > 3MB (imagens nanobanana são menores)
2. ✅ Nomes com underscore (`slide_1.png`)
3. ✅ Pasta correta do tema
4. ✅ Dimensões 1080x1350px

### 7. 📁 NOVO ASSUNTO - REGRA DE PASTA
1. **Criar pasta primeiro**: `slides/NOME-DO-TEMA/`
2. **Atualizar modelo_instagram.py**: Alterar `output_file` para a nova pasta
3. **Atualizar export_veronica_node.js**: Alterar paths para a nova pasta
4. **Gerar e exportar**: Processo normal
5. **Restaurar configs**: Após usar, restaurar para `reeducacao-alimentar/`

### 8. 📝 LEGENDA - REGRA OBRIGATÓRIA

**Após gerar, SEMPRE editar manualmente a `legenda.txt`**

Formato obrigatório:
```
@veronicabomfim.nutri

[TÍTULO DO CARROSSEL]

📌 Descrição:
[Adicionar descrição breve sobre o tema]

📝 Resumo:
• [Ponto 1 relevante]
• [Ponto 2 relevante]
• [Ponto 3 relevante]
• [Ponto 4 relevante]

📚 Fontes:
[Adicionar fontes - ex: Ministério da Saúde, OMS, estudos científicos]

🏷️ Hashtags:
#[TEMA_PRINCIPAL] #nutrição #saúde #alimentação #[TAGS_RELEVANTES]

📞 Contato:
📱 (81) 9 9864-5846
📧 veronicabomfim.nutri@gmail.com
📸 @veronicabomfim.nutri
```

### 9. 🖼️ CTA FINAL - REGRA OBRIGATÓRIA
**APÓS criar qualquer novo carrossel, SEMPRE adicionar o CTA image como último slide**

- **IMAGEM**: Usar `Imagens/CTA/CTA.png`
- **POSIÇÃO**: Sempre como slide final (após todos os conteúdos)
- **IDENTIDADE VISUAL**: Aplicar identidade visual da marca:
  - Gradiente verde na base (#394233)
  - Imagem posicionada para mostrar o rosto (object-position: 50% 55%)
  - **SEM divisor dourado** (barra #bf9566 removida para visual mais limpo)
- **NUNCA ESQUECER**: Esta regra NÃO pode ser violada

### 10. 🔄 PROCESSO CORRETO
```bash
# 1. Gerar HTML
python3 modelo_instagram.py "Título" "Subtítulo"

# 2. Exportar slides  
node export_veronica_node.js

# 3. Verificar qualidade
ls -lh slides/NOME-DO-TEMA/slide_1.png
file slides/NOME-DO-TEMA/slide_1.png

# 4. EDITAR LEGENDA - Obrigatório!
# Editar slides/NOME-DO-TEMA/legenda.txt
# Preencher: Descrição, Resumo (4 pontos), Fontes, Hashtags

# 5. ADICIONAR CTA FINAL - Obrigatório!
# Substituir último slide pelo CTA (Imagens/CTA/CTA.png)
# Aplicar identidade visual da marca

# 6. Re-exportar o slide final
# Atualizar contagem de slides se necessário

# 7. Postar no Instagram!
```

**VIOLAÇÃO DESTAS REGRAS = SLIDES NÃO FUNCIONAM NO INSTAGRAM**