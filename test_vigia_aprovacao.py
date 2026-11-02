#!/usr/bin/env python3
"""Testes do classificador do vigia de aprovação.

O risco aqui é falso positivo: o e-mail de aprovação contém as palavras
APROVAR e REJEITAR nas instruções, e o Gmail cita a mensagem original na
resposta. Se o vigia errar, um post vai para o Instagram sem aprovação.

    python3 test_vigia_aprovacao.py
"""

import unittest

from vigia_aprovacao import classificar

INSTRUCOES = (
    "<div>Responda só com a palavra <strong>APROVAR</strong> para publicar.</div>"
    "<div>Responda <strong>REJEITAR</strong> + o que corrigir.</div>"
)
CITACAO = f"<div class='gmail_quote'>{INSTRUCOES}</div>"


def mensagem(corpo):
    return {"messageText": corpo}


class ClassificadorTest(unittest.TestCase):
    def test_aprovar_simples(self):
        self.assertEqual(classificar(mensagem(f"<div>APROVAR</div>{CITACAO}")), ("aprovado", ""))

    def test_aprovar_minusculo(self):
        self.assertEqual(classificar(mensagem(f"<div>aprovar</div>{CITACAO}")), ("aprovado", ""))

    def test_aprovar_com_comentario(self):
        self.assertEqual(
            classificar(mensagem(f"<div>APROVAR, pode publicar!</div>{CITACAO}")),
            ("aprovado", ""),
        )

    def test_aprovar_entre_aspas(self):
        self.assertEqual(classificar(mensagem(f"<div>“Aprovar”</div>{CITACAO}")), ("aprovado", ""))

    def test_aprovar_depois_de_saudacao(self):
        self.assertEqual(
            classificar(mensagem(f"<div>Oi, tudo bem?</div><div>APROVAR</div>{CITACAO}")),
            ("aprovado", ""),
        )

    def test_rejeitar_com_motivo(self):
        corpo = f"<div>REJEITAR</div><div>A capa ficou escura</div>{CITACAO}"
        self.assertEqual(
            classificar(mensagem(corpo)), ("rejeitado", "A capa ficou escura")
        )

    def test_rejeitar_linha_unica(self):
        self.assertEqual(
            classificar(mensagem(f"<div>REJEITAR slide 4</div>{CITACAO}")),
            ("rejeitado", "slide 4"),
        )

    def test_rejeitar_em_blockquote_nao_conta(self):
        corpo = f"<div>REJEITAR slide 4</div><blockquote>{INSTRUCOES}</blockquote>"
        self.assertEqual(classificar(mensagem(corpo)), ("rejeitado", "slide 4"))

    def test_so_citacao_nao_e_veredito(self):
        self.assertIsNone(classificar(mensagem(CITACAO)))

    def test_conversa_nao_e_veredito(self):
        self.assertIsNone(classificar(mensagem(f"<div>Depois eu vejo</div>{CITACAO}")))

    def test_negacao_nao_e_veredito(self):
        self.assertIsNone(classificar(mensagem(f"<div>Não aprovar ainda</div>{CITACAO}")))

    def test_aprovar_no_meio_da_frase_nao_conta(self):
        corpo = f"<div>vou aprovar depois</div>{CITACAO}"
        self.assertIsNone(classificar(mensagem(corpo)))

    def test_conversa_longa_com_aprovar_nao_conta(self):
        corpo = (
            "<div>Oi! Vi o carrossel e gostei do texto, mas antes quero conferir o "
            "slide 3 com calma e ver como fica no celular. Depois disso eu vou "
            "aprovar com certeza.</div>" + CITACAO
        )
        self.assertIsNone(classificar(mensagem(corpo)))

    def test_texto_puro(self):
        corpo = (
            "APROVAR\n\nEm seg, 2 de nov de 2026 às 19:38, VERONICA escreveu:\n"
            "> Responda APROVAR ou REJEITAR"
        )
        self.assertEqual(classificar(mensagem(corpo)), ("aprovado", ""))

    def test_texto_puro_so_citacao(self):
        corpo = (
            "\nEm seg, 2 de nov de 2026 às 19:38, VERONICA escreveu:\n"
            "> Responda APROVAR ou REJEITAR"
        )
        self.assertIsNone(classificar(mensagem(corpo)))

    def test_snippet_sem_corpo_completo(self):
        # fallback quando o corpo grande não vem pelo proxy
        snippet = (
            "Aprovar Atenciosamente, Em dom., 1 de nov. de 2026 23:16, VERONICA "
            "&lt;x@gmail.com&gt; escreveu: Aprovação de conteúdo"
        )
        self.assertEqual(
            classificar({"messageText": "", "snippet": snippet}), ("aprovado", "")
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
