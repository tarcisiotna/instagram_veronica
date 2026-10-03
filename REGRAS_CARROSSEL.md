# REGRAS PADRÃO - Criação de Carrosséis Instagram

## 📋 REGRAS QUE NÃO PODEM SER VIOLADAS

### 1. 🎨 CRIAÇÃO DO CARROSSEL

- **SCRIPT**: Usar APENAS `modelo_instagram.py` ou criar HTML manualmente
- **NOME DO ARQUIVO**: Gerar SEMPRE como `carousel.html`
- **DIMENSÕES**: Manter HTML em 420px de largura (export scale para 1080px)
- **FOTO SLIDE 1**: Usar foto da pasta `Imagens/nanobanana/` — **NUNCA repetir** a foto usada no carrossel anterior. Usar SEMPRE `imagem_capa.py` (`escolher_imagem_capa(tema="NOME-DO-TEMA")`), que registra as fotos usadas em `imagens_usadas.json` e escolhe automaticamente uma foto diferente
- **VERIFICAR CAPA**: Antes de gerar, conferir `imagens_usadas.json` — a foto da capa de cada carrossel deve ser diferente
- **DESIGN**: Adaptar conforme o assunto/tema informado
- **IDENTIDADE MARCA**: Livre para usar guia da marca conforme necessidade
- **CTA FINAL**: Sempre usar `CTA.png` como último slide (slide_8)

### 2. 📸 EXPORT DOS SLIDES  
- **SCRIPT**: Usar APENAS `export_veronica_node.js` (scale factor 2.5714)
- **NOMENCLATURA**: `slide_1.png`, `slide_2.png`... (com UNDERSCORE, não hífen)
- **QUALIDADE**: deviceScaleFactor = 2.5714 (1080/420 = 2.5714x)
- **PASTA**: Salvar na pasta específica do tema (ex: `slides/reeducacao-alimentar/`)
- **BARRA DE PROGRESSO**: O script adiciona automaticamente a barra em todos os slides (slide 1 a N mostra "1/N", último slide mostra "Fim")

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

⚠️ **O contato deve conter TODOS os 4 itens abaixo: telefone, email, Instagram e site**

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
🌐 https://veronicabomfimnutriweb.pages.dev/
```

### 9. 🖼️ CTA FINAL - REGRA OBRIGATÓRIA
**APÓS criar qualquer novo carrossel, SEMPRE adicionar o CTA image como último slide**

- **IMAGEM**: Usar `Imagens/CTA/CTA.png`
- **POSIÇÃO**: Sempre como slide final (após todos os conteúdos)
- **IDENTIDADE VISUAL**:
  ```html
  <div class="slide" style="display:flex;flex-direction:column;justify-content:center;align-items:center;padding:0;overflow:hidden;position:relative;">
    <img src="{cta_b64}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;">
    <div style="position:absolute;bottom:0;left:0;right:0;padding:30px 20px;background:linear-gradient(to top,rgba(57,66,51,0.95),rgba(57,66,51,0.7),transparent);text-align:center;">
    </div>
  </div>
  ```
  - **Apenas CTA.png como fundo**, sem overlay de texto — o PNG já contém todos os elementos visuais (logo, headline, botão, contato)
  - Gradiente verde vazio na base (#394233) para legibilidade
  - **SEM overlay de texto** (sem "V", sem "Pronto para...", sem "Agendar", sem telefone/email)
  - **SEM divisor dourado** (barra #bf9566 removida para visual mais limpo)
  - **SEM barra de progresso no HTML** (o export adiciona automaticamente)
- **NUNCA ESQUECER**: Esta regra NÃO pode ser violada
- **Modelo de referência**: `slides/canetas-emagrecedoras/carousel.html` (slide 8) e `modelo_instagram.py`

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
# Seguir IDENTIDADE VISUAL da regra 9:
#   - Apenas CTA.png como fundo + gradiente verde vazio na base
#   - SEM overlay de texto, SEM barra dourada

# 6. Re-exportar o slide final
# Atualizar contagem de slides se necessário

# 7. Postar no Instagram!
```

### 11. 📊 BARRA DE PROGRESSO - PADRÃO OBRIGATÓRIO

**🚫 NÃO incluir barra de progresso no HTML do modelo_instagram.py**
- O script `export_veronica_node.js` adiciona automaticamente a barra em TODOS os slides
- Incluir no HTML causa **duas barras sobrepostas** no slide exportado
- Manter o HTML limpo, sem `<div class="progress-bar">` ou barras inline
- Exceção: a função `progress_bar()` pode existir no código, mas **não ser chamada** nos slides
- A barra no slide CTA também deve ser removida — o export cuida dela

**Modelo de referência**: `/home/tarcisio/instagram_veronica/slides/como-saber-se-caneta-e-falsa/`

A barra de progresso deve seguir este padrão em TODOS os carrosséis:

**Estrutura HTML:**
```html
<div class="progress-bar">
  <div class="progress-track"><div class="progress-fill" style="width:XX%;"></div></div>
  <span class="progress-label">N/7</span>
</div>
<div class="swipe-arrow">
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
    <path d="M9 6l6 6-6 6" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
</div>
```

**CSS obrigatório (padrão caneta-e-falsa):**
```css
.progress-bar { position: absolute; bottom: 0; left: 0; right: 0; padding: 16px 28px 20px; z-index: 10; display: flex; align-items: center; gap: 10px; background: linear-gradient(to top,rgba(0,0,0,0.7),transparent); }
.progress-track { flex: 1; height: 3px; background: rgba(255,255,255,0.12); border-radius: 2px; overflow: hidden; }
.progress-fill { height: 100%; background: #fff; border-radius: 2px; }
.progress-label { font-size: 11px; color: rgba(255,255,255,0.4); font-weight: 500; }
.swipe-arrow { position: absolute; right: 0; top: 0; bottom: 0; width: 48px; z-index: 9; display: flex; align-items: center; justify-content: center; background: linear-gradient(to right,transparent,rgba(255,255,255,0.08)); }
```

**Regras específicas:**
- **Track**: 3px altura, cor `rgba(255,255,255,0.12)` ou `rgba(0,0,0,0.08)` (slides claros)
- **Fill**: Cor dourada da marca `#bf9566` (sempre sólido, sem gradiente)
- **Gradiente de fundo**: `linear-gradient(to top,rgba(0,0,0,0.7),transparent)` abaixo da barra
- **Padding**: 16px 28px 20px
- **Swipe arrow**: Gradient fade na lateral direita + chevron sutil (remover no último slide)
- **Último slide (CTA)**: Barra 100%, label "Fim", SEM swipe arrow
- **Visibilidade CTA**: Barra deve ter bom contraste — verificar em background escuro

**VIOLAÇÃO DESTAS REGRAS = SLIDES NÃO FUNCIONAM NO INSTAGRAM**