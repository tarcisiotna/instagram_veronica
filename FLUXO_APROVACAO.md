# Fluxo de aprovação por e-mail

Todo carrossel passa por aprovação antes de ir para o Instagram. A aprovação
acontece **respondendo o e-mail**, sem botões e sem servidor.

## Por que não botão

Um botão de e-mail é só um link. Para ele publicar de verdade precisaria de um
endpoint hospedado (Worker, função, servidor) que recebesse o clique e chamasse
a API do Instagram. Optamos por não manter infraestrutura: o e-mail recebe a
resposta e o **vigia** (que já roda a cada 5 minutos) lê a resposta e publica.

## Regra que evita o erro de 24h

O Instagram expira containers de mídia em **24 horas**. Por isso **nada é criado
na API antes da aprovação**. O e-mail só carrega as URLs das imagens e a
legenda; os containers e o publish são criados pelo vigia **depois** do
"APROVAR". Assim, um e-mail respondido dois dias depois continua funcionando, e
um "REJEITAR" não deixa lixo na conta.

## Etapas

### 1. Montar o carrossel

Seguir `REGRAS_CARROSSEL.md` normalmente:

```bash
python3 gerar_<tema>.py
node export_veronica_node.js slides/<tema>/carousel.html slides/<tema>
```

Escrever `slides/<tema>/legenda.txt` no formato padrão (descrição, 4 pontos,
fontes, hashtags, contatos).

### 2. Preparar a aprovação

```bash
python3 aprovacao.py preparar <tema>
```

O script:

- publica os arquivos de mídia em `publicado/<tema>/` e versiona no GitHub
  (repo público `tarcisiotna/instagram_veronica`), virando URL `raw.githubusercontent.com`
- valida que a URL devolve imagem (HTTP 200 e tamanho > 0) antes de seguir
- usa o catbox.moe apenas como fallback (hoje está com uploads pausados)
- cria `aprovacoes/<tema>.json` com status `pendente`
- gera `aprovacoes/<tema>-email.html` com os slides, a legenda e as instruções

Nada é enviado ao Instagram.

### 3. Enviar o e-mail

Enviar `aprovacoes/<tema>-email.html` via `GMAIL_SEND_EMAIL` com `is_html=True`
para `veronicabomfim.nutri@gmail.com`, assunto `[Aprovação] <título>`.

Depois de enviar, registrar o thread:

```bash
python3 aprovacao.py marcar <tema> pendente --thread-id <threadId>
```

### 4. Ler a resposta

```bash
python3 aprovacao.py listar
```

Buscar o thread no Gmail (`GMAIL_LIST_THREADS` → `GMAIL_FETCH_MESSAGE_BY_THREAD_ID`)
e ler a última mensagem.

- resposta contendo **APROVAR** → `python3 aprovacao.py marcar <tema> aprovado --message-id <id>`
- resposta contendo **REJEITAR** → `python3 aprovacao.py marcar <tema> rejeitado --detalhe "<motivo>"`
- qualquer outra coisa, ou nenhuma resposta → continua `pendente`

#### Vigia automático (a cada 5 minutos)

O `vigia_aprovacao.py` faz essa leitura sozinho, para todos os temas com
status `pendente` — e também retoma a publicação dos que ficaram `aprovado`
por alguma falha:

```bash
python3 vigia_aprovacao.py              # verifica uma vez
python3 vigia_aprovacao.py --dry-run    # mostra o que faria, sem alterar nada
python3 vigia_aprovacao.py --loop       # fica rodando (padrão: 300s)
python3 vigia_aprovacao.py --slug novembro-azul
```

Ele lê o thread pelo MCP do Composio, ignora rascunhos e a citação do e-mail
original, e só aceita o veredito quando **APROVAR** ou **REJEITAR** abre a
resposta (ou alguma linha dela, em resposta curta). Conversa solta não muda o
status. Ao encontrar o veredito, chama `aprovacao.py marcar`.

- **APROVAR** → marca `aprovado` e **publica no Instagram na mesma passada**
  (`publicar_instagram.py`): cria os containers filhos, o container pai com a
  legenda aprovada, publica e registra `media_id`/`permalink`.
- **REJEITAR** → marca `rejeitado` e não toca na API do Instagram.

Se o publish falhar (rede, container ainda processando, limite da API), o tema
fica `aprovado` com o erro em `publicacao.erro` e o vigia tenta de novo nos
próximos ciclos, até 5 tentativas. Depois disso marca `publicacao.desistiu` e
avisa para publicar manualmente. O container criado numa tentativa anterior é
reaproveitado enquanto estiver dentro das 24h.

Para desligar só a publicação automática (o vigia continua lendo o e-mail e
marcando o status):

```bash
python3 vigia_aprovacao.py --once --sem-publicar
```

### Concorrência

O timer do systemd e uma chamada manual podem coincidir. Para isso, o vigia
segura uma trava de arquivo (`aprovacoes/.vigia.lock`, `fcntl.flock`) durante
toda a execução: se já existe um vigia rodando, o novo sai imediatamente sem
publicar nada. Assim nunca há dois processos publicando o mesmo tema.

O log fica em `aprovacoes/vigia.log`, e cada tema guarda o histórico da última
checagem em `aprovacoes/<tema>.json` (chaves `vigia` e `publicacao`).

Para deixar rodando a cada 5 minutos:

```bash
./instalar_vigia.sh              # timer do systemd (usuário)
./instalar_vigia.sh --remover    # desliga e remove
loginctl enable-linger "$USER"   # opcional: rodar mesmo sem sessão aberta
```

Alternativa sem systemd:

```bash
*/5 * * * * cd /caminho/do/repo && /usr/bin/python3 vigia_aprovacao.py --once --silencioso
```


### 5. Publicar

Acontece **automaticamente** quando o vigia encontra o `APROVAR` (veja acima).
O `publicar_instagram.py`:

1. valida a legenda (até 2.200 caracteres e 30 hashtags) e a quantidade de
   imagens (1 para post único, 2 a 10 para carrossel)
2. cria um container `is_carousel_item` por slide, na ordem
3. espera todos os containers filhos ficarem `FINISHED`
4. cria o container pai (`media_type=CAROUSEL`) com a legenda salva
5. espera o pai ficar `FINISHED`, publica e busca o `permalink`
6. registra `status: publicado` e o bloco `publicacao` no JSON do tema

A publicação usa a **Graph API** (`graph.instagram.com/v21.0`) pelo proxy do
Composio (`COMPOSIO_PROXY_EXECUTE`). As tools prontas de carrossel do Composio
(`INSTAGRAM_CREATE_CAROUSEL_CONTAINER`) recusam os containers com *"Invalid
parameter in carousel request"* mesmo com filhos válidos — por isso o caminho
direto pela Graph API. A legenda vai no corpo JSON do POST (não na query string),
porque uma legenda longa com quebras de linha quebra a URL do proxy.

Se precisar publicar manualmente (por exemplo, depois de o vigia desistir):

```bash
python3 publicar_instagram.py <tema> --dry-run   # só valida, sem chamar a API
python3 publicar_instagram.py <tema>             # publica de verdade
```

Ou, se a publicação já foi feita por fora, só registre o resultado:

```bash
python3 aprovacao.py publicar <tema> --media-id <id> --permalink <url>
python3 topic_manager.py add "<tema>"
```

## Estados

| Status | Significado |
|---|---|
| `pendente` | e-mail enviado, aguardando resposta |
| `aprovado` | resposta recebida; publicação automática em andamento ou aguardando nova tentativa |
| `rejeitado` | resposta com correções, não publica |
| `publicado` | já está no Instagram (`publicacao.media_id` e `permalink` preenchidos) |
| `cancelado` | descartado antes de publicar |

## Observações

- As imagens ficam no repositório GitHub público (`publicado/<tema>/`), servidas
  por `raw.githubusercontent.com` — links permanentes, sem prazo. O repositório
  precisa estar **público** para o Gmail e o Instagram baixarem as imagens.
- Se o link cair ou a imagem mudar, rodar `python3 aprovacao.py preparar <tema> --reupload`.
- O `aprovacoes/*.json` guarda a legenda inteira, então o post pode ser
  publicado semanas depois sem depender dos arquivos originais.
- Reenviar o e-mail depois de um `rejeitado` é só corrigir os slides, rodar
  `preparar --reupload` e enviar de novo.
- Se o vigia marcar `publicacao.desistiu`, confira o erro em
  `aprovacoes/<tema>.json`, publique manualmente com `publicar_instagram.py` e
  registre o resultado com `aprovacao.py publicar`. Para tentar de novo pelo
  vigia, remova a chave `desistiu` e zere `tentativas` no bloco `publicacao`.
