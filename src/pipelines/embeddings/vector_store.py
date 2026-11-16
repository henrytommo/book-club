import json
from pathlib import Path

import numpy as np

STORE_DIR = Path(__file__).resolve().parents[3] / "data" / "embeddings" / "vector_store"


def save(embeddings, titles, texts):
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    np.save(STORE_DIR / "embeddings.npy", embeddings)
    metadata = [{"title": title, "text": text} for title, text in zip(titles, texts)]
    (STORE_DIR / "metadata.json").write_text(json.dumps(metadata, indent=2))


def load():
    embeddings = np.load(STORE_DIR / "embeddings.npy")
    metadata = json.loads((STORE_DIR / "metadata.json").read_text())
    return embeddings, metadata
