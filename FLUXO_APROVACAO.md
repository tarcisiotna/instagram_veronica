# Fluxo de aprovação por e-mail

Todo carrossel passa por aprovação antes de ir para o Instagram. A aprovação
acontece **respondendo o e-mail**, sem botões e sem servidor.

## Por que não botão

Um botão de e-mail é só um link. Para ele publicar de verdade precisaria de um
endpoint hospedado (Worker, função, servidor) que recebesse o clique e chamasse
a API do Instagram. Optamos por não manter infraestrutura: o e-mail recebe a
resposta e a publicação acontece na sessão seguinte.

## Regra que evita o erro de 24h

O Instagram expira containers de mídia em **24 horas**. Por isso **nada é criado
na API antes da aprovação**. O e-mail só carrega as URLs das imagens e a
legenda; os containers e o publish são criados depois do "APROVAR". Assim, um
e-mail respondido dois dias depois continua funcionando, e um "REJEITAR" não
deixa lixo na conta.

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

- sobe os `slide_*.png` para o catbox.moe e guarda as URLs
- cria `aprovacoes/<tema>.json` com status `pendente`
- gera `aprovacoes/<tema>-email.html` com os 8 slides, a legenda e as instruções

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

### 5. Publicar

Só com status `aprovado`:

1. criar os N containers `carousel_item` com as URLs salvas
2. criar o container pai com a legenda salva
3. publicar
4. registrar:

```bash
python3 aprovacao.py publicar <tema> --media-id <id> --permalink <url>
python3 topic_manager.py add "<tema>"
```

## Estados

| Status | Significado |
|---|---|
| `pendente` | e-mail enviado, aguardando resposta |
| `aprovado` | resposta recebida, pode publicar |
| `rejeitado` | resposta com correções, não publica |
| `publicado` | já está no Instagram |
| `cancelado` | descartado antes de publicar |

## Observações

- As imagens ficam no catbox.moe (links permanentes, sem prazo). Se o link cair,
  rodar `python3 aprovacao.py preparar <tema> --reupload`.
- O `aprovacoes/*.json` guarda a legenda inteira, então o post pode ser
  publicado semanas depois sem depender dos arquivos originais.
- Reenviar o e-mail depois de um `rejeitado` é só corrigir os slides, rodar
  `preparar --reupload` e enviar de novo.
