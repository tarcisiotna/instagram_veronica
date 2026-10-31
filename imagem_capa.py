import json
import random
from pathlib import Path

BASE_DIR = Path(__file__).parent
TRACKING_FILE = BASE_DIR / "imagens_usadas.json"


def _load_tracking():
    if TRACKING_FILE.exists():
        return json.loads(TRACKING_FILE.read_text(encoding="utf-8"))
    return {"usadas": [], "historico": []}


def _save_tracking(data):
    TRACKING_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def escolher_imagem_capa(tema=None):
    """Escolhe uma imagem para a capa (slide 1) sem repetir fotos já usadas.

    Regra importante: cada carrossel deve usar uma foto inicial diferente.
    Quando todas as fotos disponíveis já foram usadas, o ciclo reinicia.
    """
    nanobanana_dir = BASE_DIR / "Imagens" / "nanobanana"
    imgs = sorted(
        [p for p in list(nanobanana_dir.glob("*.jpeg")) + list(nanobanana_dir.glob("*.jpg")) if p.stat().st_size > 50_000],
        key=lambda p: p.name,
    )
    if not imgs:
        return None

    data = _load_tracking()
    usadas = set(data.get("usadas", []))

    disponiveis = [p for p in imgs if p.name not in usadas]
    if not disponiveis:
        data["usadas"] = []
        usadas = set()
        disponiveis = imgs

    escolhida = random.choice(disponiveis)

    usadas.add(escolhida.name)
    data["usadas"] = sorted(usadas)
    data["historico"] = data.get("historico", [])
    data["historico"].append({"imagem": escolhida.name, "tema": tema or "desconhecido"})
    _save_tracking(data)

    return escolhida
