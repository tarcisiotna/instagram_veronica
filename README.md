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
   # Instale as dependências necessárias (ex: pip install playwright)
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
python create_veronica_carousel.py
```

### Exportação de Slides
Use os scripts de exportação para gerar os slides em PNG para o Instagram:
```bash
node export-slides.js
# ou
python export_veronica.py
```

## Fluxo de Trabalho
Após postar um assunto no Instagram, registre-o executando `python topic_manager.py add "assunto"` ou avise ao assistente "postei o assunto [assunto]" para atualização automática.

## Estrutura do Projeto
- `topic_manager.py`: Script para controle de assuntos postados
- `posted_topics.json`: Banco de dados de assuntos já publicados
- `create_veronica_carousel.py`: Gera HTML de carrossel para Instagram
- `export-*.js` / `export_*.py`: Scripts para exportar slides para PNG
- `.gitignore`: Exclui arquivos grandes (HTML, slides, imagens) do repositório

## Repositório
https://github.com/engsw-gcm-master/instagram_veronica
