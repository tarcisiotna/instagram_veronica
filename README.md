# Instagram Veronica

Ferramenta para gerar carrosséis do Instagram e controlar assuntos já postados, evitando duplicidade de conteúdo.

## Funcionalidades
- Geração de carrosséis personalizados para Instagram (1080×1350px, prévia em HTML swipável)
- Controle de assuntos já postados com data e observações
- Exportação de slides para PNG usando scripts baseados em Playwright
- Verificação de duplicidade antes de criar novo conteúdo

## Pré-requisitos
- Python 3.8+
- Node.js 16+ (para exportação de slides)
- Git

## Configuração
1. Clone o repositório:
   ```bash
   git clone https://github.com/engsw-gcm-master/instagram_veronica.git
   cd instagram_veronica
   ```
2. Configure o ambiente Python:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   ```
3. Configure as dependências Node.js (para exportação):
   ```bash
   npm install
   ```

## Uso

### Controle de Assuntos Postados
Gerencie os temas já publicados no Instagram:
- Verificar se um assunto já foi postado:
  ```bash
  python topic_manager.py check "canetas emagrecedoras"
  ```
- Registrar um novo assunto postado:
  ```bash
  python topic_manager.py add "novo assunto"
  ```
- Listar todos os assuntos já postados:
  ```bash
  python topic_manager.py list
  ```

### Criação de Carrosséis
Execute os scripts de geração de carrossel para criar prévias em HTML:
```bash
python modelo_instagram.py "Título" "Subtítulo"
# ou
python gerar_carousel.py
# ou
python gerar_sarcopenia.py
```

### Exportação de Slides
Use os scripts de exportação para gerar os slides em PNG para o Instagram:
```bash
node export_veronica_node.js
# ou
python export_slides.py
```

### Verificação de Regras
Antes de exportar, verifique se o carrossel segue todas as regras:
```bash
python verificar_carrossel.py slides/nome-do-tema
```

## Fluxo de Trabalho
Após postar um assunto no Instagram, registre-o executando `python topic_manager.py add "assunto"` ou avise ao assistente "postei o assunto [assunto]" para atualização automática.

## Estrutura do Projeto
- `topic_manager.py`: Script para controle de assuntos postados
- `posted_topics.json`: Banco de dados de assuntos já publicados
- `modelo_instagram.py`: Gera HTML de carrossel "Mitos e Verdades"
- `gerar_carousel.py`: Gera HTML de carrossel "Nutrição Oncológica"
- `gerar_sarcopenia.py`: Gera HTML de carrossel "Sarcopenia"
- `export_veronica_node.js`: Exporta slides para PNG (Node.js + Playwright)
- `export_slides.py`: Exporta slides para PNG (Python + Playwright)
- `verificar_carrossel.py`: Verifica regras do carrossel antes de exportar
- `.gitignore`: Exclui arquivos grandes (HTML, slides, imagens) do repositório

## Repositório
https://github.com/engsw-gcm-master/instagram_veronica
