#!/usr/bin/env python3
"""Testes do classificador do vigia de aprovação.

O risco aqui é falso positivo: o e-mail de aprovação contém as palavras
APROVAR e REJEITAR nas instruções, e o Gmail cita a mensagem original na
resposta. Se o vigia errar, um post vai para o Instagram sem aprovação.

    python3 test_vigia_aprovacao.py
"""

import unittest

from vigia_aprovacao import (
    EMAIL_DONO,
    classificar,
    indice_da_aprovacao,
    remetente_permitido,
)

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


class AprovacaoAdiadaTest(unittest.TestCase):
    """APROVAR com dúvida, negação ou adiamento não publica nada."""

    def test_aprovar_depois_nao_aproveita(self):
        self.assertIsNone(classificar(mensagem(f"<div>APROVAR depois</div>{CITACAO}")))

    def test_aprovar_com_interrogacao_nao_aproveita(self):
        self.assertIsNone(classificar(mensagem(f"<div>APROVAR?</div>{CITACAO}")))

    def test_aprovar_negado_nao_aproveita(self):
        self.assertIsNone(
            classificar(mensagem(f"<div>APROVAR, não agora</div>{CITACAO}"))
        )

    def test_aprovar_para_depois_nao_aproveita(self):
        self.assertIsNone(
            classificar(mensagem(f"<div>Aprovar só mais tarde</div>{CITACAO}"))
        )

    def test_aprovar_com_certeza_aprova(self):
        self.assertEqual(
            classificar(mensagem(f"<div>APROVAR, pode publicar!</div>{CITACAO}")),
            ("aprovado", ""),
        )


class RemetenteTest(unittest.TestCase):
    """Só a conta da proprietária pode aprovar."""

    def test_remetente_da_proprietaria_e_aceito(self):
        self.assertTrue(
            remetente_permitido({"remetente": f"Veronica Bomfim <{EMAIL_DONO}>"})
        )

    def test_outro_remetente_e_recusado(self):
        self.assertFalse(
            remetente_permitido({"remetente": "Alguem <alguem@example.com>"})
        )

    def test_sem_remetente_e_recusado(self):
        self.assertFalse(remetente_permitido({}))


class IndiceDaAprovacaoTest(unittest.TestCase):
    """O e-mail de aprovação precisa ser identificado — senão, fail-safe."""

    def thread(self):
        return [
            {"messageId": "aaaa1111", "labelIds": ["SENT"], "internalDate": 100},
            {"messageId": "bbbb2222", "labelIds": ["INBOX"], "internalDate": 200},
        ]

    def test_usa_thread_id_registrado(self):
        # No Gmail o id do thread é o id da primeira mensagem (o e-mail de
        # aprovação). O message_id guardado é o da resposta — não serve de
        # âncora.
        dados = {"email": {"thread_id": "aaaa1111", "message_id": "bbbb2222"}}
        self.assertEqual(indice_da_aprovacao(self.thread(), dados), 0)

    def test_sem_thread_id_usa_a_primeira_mensagem(self):
        self.assertEqual(indice_da_aprovacao(self.thread(), {}), 0)

    def test_primeira_mensagem_de_outro_remetente_nao_serve(self):
        mensagens = [
            {"messageId": "aaaa1111", "labelIds": ["INBOX"], "internalDate": 100},
            {"messageId": "bbbb2222", "labelIds": ["INBOX"], "internalDate": 200},
        ]
        self.assertIsNone(indice_da_aprovacao(mensagens, {}))

    def test_thread_id_sem_correspondencia_usa_a_primeira(self):
        dados = {"email": {"thread_id": "cccc3333"}}
        self.assertEqual(indice_da_aprovacao(self.thread(), dados), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
