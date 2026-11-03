#!/usr/bin/env python3
"""Testes do publicador automático e da integração com o vigia.

Nenhum teste chama o Instagram de verdade: `_graph` é sempre substituído por
um dublê que emula a Graph API. O que importa é a ordem das chamadas, os
argumentos (legenda crua, children na ordem dos slides) e a idempotência.

    python3 test_publicar_instagram.py
"""

import unittest
from datetime import datetime, timedelta
from unittest import mock

import publicar_instagram
import vigia_aprovacao
from composio_mcp import ErroFerramenta

LEGENDA = (
    "📷 @veronicabomfim.nutri\n"
    "Título do post\n\n"
    "📌 Descrição:\nTexto aprovado.\n\n"
    "#nutricao #saude"
)


def dados_base(**extras):
    dados = {
        "slug": "teste",
        "tipo": "carousel",
        "titulo": "Título do post",
        "status": "aprovado",
        "legenda": LEGENDA,
        "imagens": [
            f"https://raw.githubusercontent.com/tarcisiotna/instagram_veronica/"
            f"master/publicado/teste/slide_{i}.png"
            for i in range(1, 4)
        ],
    }
    dados.update(extras)
    return dados


class Duble:
    """Dublê da Graph API do Instagram (substitui `publicar_instagram._graph`)."""

    def __init__(self, falhar_publicacao=False, media_publicada=None):
        self.chamadas = []
        self.falhar_publicacao = falhar_publicacao
        self.media_publicada = media_publicada
        self._filhos = 0

    def __call__(self, metodo, caminho, parametros=None, corpo=None, timeout=180):
        parametros = parametros or {}
        self.chamadas.append(
            {
                "metodo": metodo,
                "caminho": caminho,
                "parametros": parametros,
                "corpo": dict(corpo or {}),
            }
        )

        if metodo == "GET":
            if caminho.endswith("/media"):
                return {"data": self.media_publicada or []}
            if "permalink" in (parametros.get("fields") or ""):
                return {
                    "id": caminho.strip("/"),
                    "permalink": "https://instagram.com/p/x/",
                }
            # status de container
            return {
                "id": caminho.strip("/"),
                "status_code": "FINISHED",
                "status": "FINISHED",
            }

        # POST
        if caminho.endswith("/media_publish"):
            if self.falhar_publicacao:
                raise ErroFerramenta("instagram", "Instagram API Error (9007)")
            return {"id": "media_123"}

        corpo = corpo or {}
        if corpo.get("is_carousel_item"):
            self._filhos += 1
            return {"id": f"filho_{self._filhos}"}
        if corpo.get("media_type") == "CAROUSEL":
            return {"id": "container_pai"}
        return {"id": "container_post"}

    def caminhos(self, metodo=None):
        return [
            (c["metodo"], c["caminho"])
            for c in self.chamadas
            if metodo is None or c["metodo"] == metodo
        ]

    def posts_media(self):
        return [c for c in self.chamadas if c["metodo"] == "POST" and c["caminho"].endswith("/media")]


class LegendaTest(unittest.TestCase):
    def test_remove_cabecalho_e_valida(self):
        legenda = publicar_instagram.legenda_do_post(dados_base())
        self.assertTrue(legenda.startswith("Título do post"))
        self.assertNotIn("📷", legenda)

    def test_recusa_legenda_longa(self):
        dados = dados_base(legenda="x" * 2201)
        with self.assertRaises(publicar_instagram.ErroPublicacao):
            publicar_instagram.legenda_do_post(dados)

    def test_recusa_hashtags_demais(self):
        dados = dados_base(legenda="post " + " ".join(f"#t{i}" for i in range(31)))
        with self.assertRaises(publicar_instagram.ErroPublicacao):
            publicar_instagram.legenda_do_post(dados)

    def test_recusa_url_de_host_nao_permitido(self):
        # Imagem de host desconhecido (rastreador/host de terceiros) não pode
        # virar o que é publicado.
        dados = dados_base(
            imagens=["https://rastreador.exemplo.com/slide_1.png"]
        )
        duble = Duble()
        with mock.patch.object(publicar_instagram, "_graph", duble):
            with self.assertRaises(publicar_instagram.ErroPublicacao):
                publicar_instagram.publicar(dados)
        self.assertEqual(duble.chamadas, [])

    def test_recusa_url_http(self):
        dados = dados_base(
            imagens=["http://raw.githubusercontent.com/x/y/slide_1.png"]
        )
        duble = Duble()
        with mock.patch.object(publicar_instagram, "_graph", duble):
            with self.assertRaises(publicar_instagram.ErroPublicacao):
                publicar_instagram.publicar(dados)
        self.assertEqual(duble.chamadas, [])


class PublicarTest(unittest.TestCase):
    def test_carrossel_cria_filhos_em_ordem_e_publica(self):
        duble = Duble()
        with mock.patch.object(publicar_instagram, "_graph", duble):
            resultado = publicar_instagram.publicar(dados_base())

        self.assertEqual(resultado["media_id"], "media_123")
        self.assertEqual(resultado["permalink"], "https://instagram.com/p/x/")
        self.assertEqual(resultado["criacao_id"], "container_pai")
        self.assertEqual(resultado["filhos"], ["filho_1", "filho_2", "filho_3"])

        posts = duble.posts_media()
        filhos = posts[:3]
        pai = posts[3]
        self.assertEqual(
            [a["corpo"]["image_url"] for a in filhos],
            dados_base()["imagens"],
        )
        self.assertTrue(all(a["corpo"]["is_carousel_item"] for a in filhos))
        self.assertEqual(pai["corpo"]["media_type"], "CAROUSEL")
        self.assertEqual(pai["corpo"]["children"], "filho_1,filho_2,filho_3")
        self.assertIn("Título do post", pai["corpo"]["caption"])

        publish = next(c for c in duble.chamadas if c["caminho"].endswith("/media_publish"))
        self.assertEqual(publish["corpo"]["creation_id"], "container_pai")

    def test_espera_filhos_finished_antes_do_pai(self):
        duble = Duble()
        with mock.patch.object(publicar_instagram, "_graph", duble):
            publicar_instagram.publicar(dados_base())

        # índice do POST que cria o container pai
        pai = next(
            i
            for i, c in enumerate(duble.chamadas)
            if c["metodo"] == "POST" and c["corpo"].get("media_type") == "CAROUSEL"
        )
        # os três containers filhos precisam ser consultados (status) antes do pai
        status_antes = [
            i
            for i, c in enumerate(duble.chamadas[:pai])
            if c["metodo"] == "GET" and "status_code" in (c["parametros"].get("fields") or "")
        ]
        self.assertEqual(len(status_antes), 3)

    def test_post_unico_usa_caption_no_container(self):
        duble = Duble()
        dados = dados_base(
            tipo="post",
            imagens=[
                "https://raw.githubusercontent.com/tarcisiotna/instagram_veronica/"
                "master/publicado/teste/post.png"
            ],
        )
        with mock.patch.object(publicar_instagram, "_graph", duble):
            resultado = publicar_instagram.publicar(dados)

        self.assertEqual(resultado["media_id"], "media_123")
        posts = duble.posts_media()
        self.assertEqual(len(posts), 1)
        self.assertIn("Título do post", posts[0]["corpo"]["caption"])
        self.assertNotIn("is_carousel_item", posts[0]["corpo"])

    def test_recusa_status_nao_aprovado(self):
        with self.assertRaises(publicar_instagram.ErroPublicacao):
            publicar_instagram.publicar(dados_base(status="pendente"))

    def test_recusa_carrossel_com_um_slide(self):
        with self.assertRaises(publicar_instagram.ErroPublicacao):
            publicar_instagram.publicar(dados_base(imagens=["https://x/1.png"]))

    def test_recusa_mais_de_dez_slides(self):
        dados = dados_base(imagens=[f"https://x/{i}.png" for i in range(11)])
        with self.assertRaises(publicar_instagram.ErroPublicacao):
            publicar_instagram.publicar(dados)

    def test_reaproveita_container_de_tentativa_anterior(self):
        duble = Duble()
        dados = dados_base(
            publicacao={
                "fase": "falha_publicacao",
                "criacao_id": "container_antigo",
                "criacao_em": datetime.now().astimezone().isoformat(timespec="seconds"),
                "filhos": ["a", "b", "c"],
            }
        )
        with mock.patch.object(publicar_instagram, "_graph", duble):
            resultado = publicar_instagram.publicar(dados)

        self.assertEqual(resultado["criacao_id"], "container_antigo")
        self.assertEqual(duble.posts_media(), [])
        publish = next(c for c in duble.chamadas if c["caminho"].endswith("/media_publish"))
        self.assertEqual(publish["corpo"]["creation_id"], "container_antigo")

    def test_recria_container_vencido(self):
        duble = Duble()
        dados = dados_base(
            publicacao={
                "fase": "falha_publicacao",
                "criacao_id": "container_velho",
                "criacao_em": (
                    datetime.now().astimezone() - timedelta(days=2)
                ).isoformat(timespec="seconds"),
                "filhos": ["a", "b", "c"],
            }
        )
        with mock.patch.object(publicar_instagram, "_graph", duble):
            resultado = publicar_instagram.publicar(dados)

        self.assertEqual(resultado["criacao_id"], "container_pai")
        self.assertEqual(len(duble.posts_media()), 4)  # 3 filhos + pai

    def test_recupera_post_quando_publish_falha_mas_saiu(self):
        duble = Duble(
            falhar_publicacao=True,
            media_publicada=[
                {
                    "id": "media_recuperada",
                    "permalink": "https://instagram.com/p/rec/",
                    "caption": publicar_instagram.legenda_do_post(dados_base()),
                    "timestamp": datetime.now().astimezone().isoformat(),
                }
            ],
        )
        with mock.patch.object(publicar_instagram, "_graph", duble):
            resultado = publicar_instagram.publicar(dados_base())

        self.assertEqual(resultado["media_id"], "media_recuperada")
        self.assertTrue(resultado["recuperado"])
        self.assertEqual(resultado["permalink"], "https://instagram.com/p/rec/")

    def test_progresso_e_persistido_por_etapa(self):
        duble = Duble()
        vistos = []
        with mock.patch.object(publicar_instagram, "_graph", duble):
            publicar_instagram.publicar(
                dados_base(), ao_progredir=lambda p: vistos.append(dict(p))
            )

        fases = [p["fase"] for p in vistos]
        self.assertIn("filhos 1/3", fases)
        self.assertIn("container_pronto", fases)
        self.assertIn("publicando", fases)
        container = next(p for p in vistos if p["fase"] == "container_pronto")
        self.assertEqual(container["criacao_id"], "container_pai")


class VigiaPublicaTest(unittest.TestCase):
    def setUp(self):
        self.dados = dados_base(status="aprovado")
        patchers = [
            mock.patch.object(vigia_aprovacao, "salvar"),
            mock.patch.object(vigia_aprovacao, "notificar"),
            mock.patch.object(vigia_aprovacao, "_registrar_topico"),
            mock.patch.object(vigia_aprovacao, "log"),
        ]
        for patcher in patchers:
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_publica_e_marca_publicado(self):
        resultado = {
            "fase": "publicado",
            "media_id": "media_123",
            "permalink": "https://instagram.com/p/x/",
            "criacao_id": "container_pai",
            "filhos": ["a", "b", "c"],
            "publicado_em": "2026-11-02T20:00:00-03:00",
        }
        with mock.patch.object(
            vigia_aprovacao.publicar_instagram, "publicar", return_value=resultado
        ) as publicar:
            ok = vigia_aprovacao._publicar_aprovado("teste", self.dados, silencioso=True)

        self.assertTrue(ok)
        publicar.assert_called_once()
        self.assertEqual(self.dados["status"], "publicado")
        self.assertEqual(self.dados["publicacao"]["media_id"], "media_123")
        self.assertEqual(self.dados["publicacao"]["tentativas"], 1)

    def test_falha_mantem_aprovado_e_conta_tentativa(self):
        with mock.patch.object(
            vigia_aprovacao.publicar_instagram,
            "publicar",
            side_effect=RuntimeError("boom"),
        ):
            ok = vigia_aprovacao._publicar_aprovado("teste", self.dados, silencioso=True)

        self.assertFalse(ok)
        self.assertEqual(self.dados["status"], "aprovado")
        self.assertEqual(self.dados["publicacao"]["tentativas"], 1)
        self.assertIn("boom", self.dados["publicacao"]["erro"])

    def test_desiste_apos_limite(self):
        self.dados["publicacao"] = {
            "tentativas": vigia_aprovacao.MAX_TENTATIVAS_PUBLICACAO
        }
        with mock.patch.object(
            vigia_aprovacao.publicar_instagram, "publicar"
        ) as publicar:
            ok = vigia_aprovacao._publicar_aprovado("teste", self.dados, silencioso=True)

        self.assertFalse(ok)
        publicar.assert_not_called()
        self.assertTrue(self.dados["publicacao"]["desistiu"])

    def test_nao_publica_em_dry_run(self):
        with mock.patch.object(
            vigia_aprovacao.publicar_instagram, "publicar"
        ) as publicar:
            ok = vigia_aprovacao._publicar_aprovado(
                "teste", self.dados, silencioso=True, dry_run=True
            )

        self.assertTrue(ok)
        publicar.assert_not_called()
        self.assertEqual(self.dados["status"], "aprovado")

    def test_verificar_dispara_publicacao_quando_aprovado(self):
        with mock.patch.object(
            vigia_aprovacao, "carregar", return_value=self.dados
        ), mock.patch.object(
            vigia_aprovacao, "_publicar_aprovado", return_value=True
        ) as publicar:
            ok = vigia_aprovacao.verificar("teste", silencioso=True)

        self.assertTrue(ok)
        publicar.assert_called_once_with("teste", self.dados, True, False)

    def test_verificar_sem_publicar_nao_chama_instagram(self):
        with mock.patch.object(
            vigia_aprovacao, "carregar", return_value=self.dados
        ), mock.patch.object(
            vigia_aprovacao, "_publicar_aprovado"
        ) as publicar:
            ok = vigia_aprovacao.verificar("teste", silencioso=True, publicar=False)

        self.assertTrue(ok)
        publicar.assert_not_called()

    def test_verificar_publicado_nao_faz_nada(self):
        self.dados["status"] = "publicado"
        with mock.patch.object(
            vigia_aprovacao, "carregar", return_value=self.dados
        ), mock.patch.object(
            vigia_aprovacao, "_publicar_aprovado"
        ) as publicar:
            ok = vigia_aprovacao.verificar("teste", silencioso=True)

        self.assertTrue(ok)
        publicar.assert_not_called()

    def test_verificar_pendente_nao_publica(self):
        self.dados["status"] = "pendente"
        with mock.patch.object(
            vigia_aprovacao, "carregar", return_value=self.dados
        ), mock.patch.object(
            vigia_aprovacao, "_publicar_aprovado"
        ) as publicar:
            vigia_aprovacao.verificar("teste", silencioso=True)

        publicar.assert_not_called()


class AlvosTest(unittest.TestCase):
    def test_alvos_por_status(self):
        pendente = dados_base(slug="pendente", status="pendente")
        aprovado = dados_base(slug="aprovado", status="aprovado")
        desistiu = dados_base(
            slug="desistiu",
            status="aprovado",
            publicacao={"desistiu": True, "tentativas": 5},
        )
        publicado = dados_base(slug="publicado", status="publicado")

        import json
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as pasta:
            base = Path(pasta)
            (base / "aprovacoes").mkdir()
            for dados in (pendente, aprovado, desistiu, publicado):
                (base / "aprovacoes" / f"{dados['slug']}.json").write_text(
                    json.dumps(dados), encoding="utf-8"
                )
            with mock.patch.object(vigia_aprovacao, "BASE_DIR", base):
                com = vigia_aprovacao.alvos(publicar=True)
                sem = vigia_aprovacao.alvos(publicar=False)

        self.assertEqual(com, ["aprovado", "pendente"])
        self.assertEqual(sem, ["pendente"])


class TravaTest(unittest.TestCase):
    """Duas execuções do vigia não podem publicar ao mesmo tempo."""

    def test_segunda_execucao_espera_ou_sai(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as pasta:
            base = Path(pasta)
            (base / "aprovacoes").mkdir()
            with mock.patch.object(vigia_aprovacao, "CAMINHO_TRAVA", base / "aprovacoes" / ".vigia.lock"):
                with vigia_aprovacao.trava_vigia() as primeira:
                    self.assertTrue(primeira)
                    with vigia_aprovacao.trava_vigia() as segunda:
                        self.assertFalse(segunda)


class FluxoCompletoTest(unittest.TestCase):
    """Ciclo real: tema aprovado → publicação → status `publicado`."""

    def test_tema_aprovado_vira_publicado(self):
        import json
        import shutil
        import tempfile
        from pathlib import Path

        import aprovacao

        base = Path(tempfile.mkdtemp())
        (base / "aprovacoes").mkdir()
        self.addCleanup(shutil.rmtree, base, True)

        dados = dados_base(slug="teste-e2e", status="aprovado")
        (base / "aprovacoes" / "teste-e2e.json").write_text(
            json.dumps(dados), encoding="utf-8"
        )

        class Publicacao:
            def __call__(self, dados, ao_progredir=None):
                return {
                    "fase": "publicado",
                    "media_id": "m1",
                    "permalink": "https://instagram.com/p/teste/",
                    "publicado_em": "2026-11-02T21:00:00-03:00",
                }

        with mock.patch.object(vigia_aprovacao, "BASE_DIR", base), mock.patch.object(
            vigia_aprovacao, "LOG_PATH", base / "aprovacoes" / "vigia.log"
        ), mock.patch.object(
            vigia_aprovacao, "CAMINHO_TRAVA", base / "aprovacoes" / ".vigia.lock"
        ), mock.patch.object(
            aprovacao, "APROV_DIR", base / "aprovacoes"
        ), mock.patch.object(
            vigia_aprovacao.publicar_instagram, "publicar", Publicacao()
        ), mock.patch.object(
            vigia_aprovacao, "notificar"
        ), mock.patch.object(
            vigia_aprovacao, "_registrar_topico"
        ):
            ok = vigia_aprovacao.verificar_todas(None, silencioso=True)

        final = json.loads(
            (base / "aprovacoes" / "teste-e2e.json").read_text(encoding="utf-8")
        )
        self.assertTrue(ok)
        self.assertEqual(final["status"], "publicado")
        self.assertEqual(final["publicacao"]["media_id"], "m1")
        self.assertEqual(final["publicacao"]["tentativas"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
