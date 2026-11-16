import json
from collections import Counter
from pathlib import Path

import numpy as np
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

STORE_DIR = Path(__file__).resolve().parents[2] / "data" / "embeddings" / "vector_store"

# openlibrary api has no genre field, so genres are matched against each book's subjects
GENRES = [
    "Romance", "Fantasy", "Science fiction", "Mystery", "Thriller", "Crime",
    "Horror", "Historical", "Biography", "Memoir", "Poetry", "Humor",
    "Young adult", "LGBTQ",
]


def most_common(books, field, n=5):
    return Counter(item for book in books.values() for item in book[field] or []).most_common(n)


def genre_counts(books):
    counts = Counter()
    for book in books.values():
        subjects = " ".join(book["subjects"] or []).lower()
        counts.update(genre for genre in GENRES if genre.lower() in subjects)
    return counts


@st.cache_data
def load_embeddings():
    embeddings = np.load(STORE_DIR / "embeddings.npy")
    titles = [book["title"] for book in json.loads((STORE_DIR / "metadata.json").read_text())]
    return embeddings, titles


@st.cache_data
def tsne_coords():
    embeddings, _ = load_embeddings()
    # perplexity must be below the number of books, and small datasets need a low one
    tsne = TSNE(n_components=2, perplexity=min(5, len(embeddings) - 1), metric="cosine", random_state=42)
    return tsne.fit_transform(embeddings)


@st.cache_data
def clusters(k):
    # cluster on the full 384-dim vectors, not the 2d projection
    embeddings, _ = load_embeddings()
    return KMeans(n_clusters=k, n_init="auto", random_state=42).fit_predict(embeddings)
