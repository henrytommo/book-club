import json
from pathlib import Path

import pandas as pd
import streamlit as st

from app_helper import genre_counts, most_common

DESCRIPTIONS_JSON = Path(__file__).resolve().parents[2] / "data" / "descriptions" / "descriptions.json"
data = json.loads(DESCRIPTIONS_JSON.read_text())

st.title("Book Club Stats")
st.metric("Books read", len(data))

st.subheader("Books by genre")
st.bar_chart(pd.Series(genre_counts(data), name="books"))

for col, (label, field) in zip(st.columns(3), [("Subject", "subjects"), ("Place", "places"), ("Time", "times")]):
    top = most_common(data, field)
    col.metric(f"Most common {label.lower()}", top[0][0] if top else "—")
    col.dataframe(pd.DataFrame(top, columns=[label, "Books"]), hide_index=True)
