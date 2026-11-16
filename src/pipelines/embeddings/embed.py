import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

from vector_store import save

DESCRIPTIONS_JSON = Path(__file__).resolve().parents[3] / "data" / "descriptions" / "descriptions.json"
FIELDS = ["subjects", "places", "times"]


def book_text(book):
    # description first, then "field: a, b, c" lines for each list field present
    lines = [book["description"]] + [f"{field}: {', '.join(book[field])}" for field in FIELDS if book[field]]
    return "\n".join(line for line in lines if line)


def main():
    data = json.loads(DESCRIPTIONS_JSON.read_text())
    texts = {title: book_text(book) for title, book in data.items()}
    texts = {title: text for title, text in texts.items() if text}

    # downloads the model on the first run, then loads from the huggingface cache
    model = SentenceTransformer("BAAI/bge-small-en-v1.5", device="mps")
    embeddings = model.encode(list(texts.values()), normalize_embeddings=True, show_progress_bar=True)

    save(embeddings, list(texts), list(texts.values()))
    print(f"Embedded {len(texts)} books")


if __name__ == "__main__":
    main()
