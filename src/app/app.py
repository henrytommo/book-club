import json
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

from app_helper import STORE_DIR, clusters, genre_counts, load_embeddings, most_common, tsne_coords

DESCRIPTIONS_JSON = Path(__file__).resolve().parents[2] / "data" / "descriptions" / "descriptions.json"
data = json.loads(DESCRIPTIONS_JSON.read_text())

st.title("Book Club Stats")
stats_tab, embeddings_tab = st.tabs(["Stats", "Embeddings"])

with stats_tab:
    st.metric("Books read", len(data))

    st.subheader("Books by genre")
    st.bar_chart(pd.Series(genre_counts(data), name="books"))

    for col, (label, field) in zip(st.columns(3), [("Subject", "subjects"), ("Place", "places"), ("Time", "times")]):
        top = most_common(data, field)
        col.metric(f"Most common {label.lower()}", top[0][0] if top else "—")
        col.dataframe(pd.DataFrame(top, columns=[label, "Books"]), hide_index=True)

with embeddings_tab:
    if not (STORE_DIR / "embeddings.npy").exists():
        st.info("Run src/pipelines/embeddings/embed.py first")
    else:
        k = st.slider("Clusters", 2, 6, 4)
        _, titles = load_embeddings()
        coords = tsne_coords()
        books = pd.DataFrame({"title": titles, "x": coords[:, 0], "y": coords[:, 1], "cluster": clusters(k)})

        # t-sne axes have no meaning, so hide them
        chart = alt.Chart(books).mark_circle(size=120).encode(
            x=alt.X("x", axis=None),
            y=alt.Y("y", axis=None),
            color="cluster:N",
            tooltip=["title", "cluster"],
        )
        st.altair_chart(chart, use_container_width=True)
