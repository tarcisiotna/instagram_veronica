# Segurança

Este repositório é **público** no GitHub. O código-fonte pode ser visto por
qualquer pessoa — o que não pode é a **credencial** que abre o Gmail e o
Instagram da conta.

## O que nunca deve ir para o repositório

| Item | Onde fica | Status |
|---|---|---|
| Chave do Composio (MCP) | `.env` ou `~/.config/opencode/opencode.json` | ignorado / fora do repo |
| Senha de app do Gmail | `.env` | ignorado / fora do repo |
| Estado das aprovações (`aprovacoes/*.json`) | máquina local | ignorado |
| HTML dos e-mails de aprovação | `aprovacoes/*-email.html` | ignorado |
| Log do vigia | `aprovacoes/vigia.log` | ignorado |

O `.gitignore` cobre `.env`, `.env.*`, chaves/credenciais comuns e todo o
conteúdo de `aprovacoes/`. O único arquivo de exemplo versionado é
`.env.example` (sem valor nenhum).

## Permissões dos arquivos de credencial

A chave do Composio dá acesso total às contas de Gmail e Instagram. O arquivo
que a guarda precisa ser legível **só pelo dono**:

```bash
chmod 600 .env
chmod 600 ~/.config/opencode/opencode.json
```

O `composio_mcp.py` recusa rodar se encontrar a chave em um arquivo legível
por grupo ou por outros usuários, e explica como corrigir.

## Regras do fluxo de aprovação

As regras abaixo existem para que um post **nunca** vá ao Instagram sem
autorização explícita da proprietária:

1. **Só a conta da proprietária aprova.** O vigia lê o cabeçalho `From` da
   resposta e ignora qualquer mensagem de outro remetente — inclusive de
   alguém para quem o e-mail foi reencaminhado.
2. **Só mensagens depois do e-mail de aprovação contam.** Se o e-mail enviado
   não for identificado no thread, o vigia falha para o lado seguro: o post
   fica `pendente` e nada é publicado.
3. **"APROVAR" precisa ser inequívoco.** Dúvida, negação ou adiamento
   ("APROVAR depois", "APROVAR?", "não APROVAR") deixam o post pendente.
4. **O e-mail de aprovação vai só para a conta da proprietária**
   (`APROVACAO_EMAIL`). Enviar para outro endereço faria quem o controla
   aprovar o post sozinho.
5. **Nada é criado na API do Instagram antes da aprovação** — os containers
   nascem só no momento do publish, dentro do prazo de 24h.

## Mídia hospedada no repositório

As imagens ficam em `publicado/<tema>/` e são servidas por
`raw.githubusercontent.com` — o repositório precisa ser **público** para o
Gmail e o Instagram conseguirem baixar os arquivos.

Consequência: **toda mídia versionada fica pública e permanente**, inclusive
a de posts que ainda não foram aprovados e a de posts rejeitados. Se um
carrossel for rejeitado, remova os arquivos de `publicado/<tema>/` do
repositório.

O fallback `catbox.moe` (host público de terceiros, fora do controle do
projeto) fica **desligado por padrão**. Para ligá-lo:

```bash
APROVACAO_ALLOW_CATBOX=1 python3 aprovacao.py preparar <tema>
```

## Upload automático

`aprovacao.py` faz `git add` + `commit` + `push` no remote `origin` para
publicar a mídia. Antes de escrever, ele confere se o remote é o esperado
(`GITHUB_REMOTE_ESPERADO`) — se for outro repositório, o script para em vez
de publicar a mídia em um lugar não revisado.

## Se um segredo vazou

1. **Revogue/rotacione imediatamente** a credencial comprometida
   (chave do Composio, senha de app do Gmail, token do Instagram).
2. **Limpe o histórico** do GitHub (Settings → Danger Zone) — só remover o
   arquivo no último commit não apaga a versão antiga.
3. **Force-push** do histórico limpo:
   `git filter-repo --invert-paths --path .env` (ou `git filter-branch`).
4. Avise quem possa ter visto a credencial: com a chave do Composio, quem
   tem acesso pode ler o Gmail e publicar na conta.

## Serviço do vigia

O timer do systemd roda com hardening (`NoNewPrivileges`, `ProtectSystem`,
`ProtectHome=read-only`, `UMask=0077`): o processo escreve somente no
diretório do projeto. Depois de mexer no arquivo de serviço, reinstale:

```bash
./instalar_vigia.sh
```
