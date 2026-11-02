# Instruções do projeto — Instagram @veronicabomfim.nutri

Leia antes de qualquer tarefa:

- `REGRAS_CARROSSEL.md` — regras que não podem ser violadas (design, export, legenda, CTA, barra de progresso)
- `FLUXO_APROVACAO.md` — fluxo de aprovação por e-mail
- `.opencode/skills/instagram-carousel/BRAND_VERONICA.md` — identidade da marca

## Fluxo obrigatório de cada carrossel

**Planejar → Construir → Enviar e-mail de aprovação → Aguardar resposta → Publicar**

1. **Planejar** — roteiro slide a slide, fontes verificadas (INCA / SBNO / ESPEN), foto da capa via `imagem_capa.py`
2. **Construir** — gerar o HTML, exportar com `export_veronica_node.js`, escrever `legenda.txt`
3. **Enviar e-mail de aprovação** — `python3 aprovacao.py preparar <tema>` e enviar via Gmail
4. **Aguardar** — o `vigia_aprovacao.py` lê a resposta a cada 5 min (veja `FLUXO_APROVACAO.md`)
5. **Publicar** — **automático** pelo vigia após resposta `APROVAR`; manual com `python3 publicar_instagram.py <tema>` se precisar

## Proibições

- **Nunca publicar no Instagram sem aprovação explícita por e-mail.**
- Nunca criar containers na API do Instagram antes da aprovação (expiram em 24h).
- Nunca publicar número/estatística sem fonte verificável.
- Nunca repetir a foto da capa do carrossel anterior.
- Nunca incluir barra de progresso no HTML — o export injeta.
- Publicar pela Graph API via `COMPOSIO_PROXY_EXECUTE` — as tools prontas de
  carrossel do Composio falham com *"Invalid parameter in carousel request"*.
- Legenda longa vai no corpo JSON do POST, nunca na query string do proxy.

## Conta

- Instagram: `@veronicabomfim.nutri` — id `28882452441414713`
- Conta Composio Instagram: `instagram_trough-anakes`
- Conta Composio Gmail: `gmail_coleen-haster` (`veronicabomfim.nutri@gmail.com`)
- E-mail de aprovação: `veronicabomfim.nutri@gmail.com`
