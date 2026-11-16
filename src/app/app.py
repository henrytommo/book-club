import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from data.data import data
from app_helper import genre_counts, most_common

st.title("Book Club Stats")
st.metric("Books read", len(data))

st.subheader("Books by genre")
st.bar_chart(pd.Series(genre_counts(data), name="books"))

for col, (label, field) in zip(st.columns(3), [("Subject", "subjects"), ("Place", "places"), ("Time", "times")]):
    top = most_common(data, field)
    col.metric(f"Most common {label.lower()}", top[0][0] if top else "—")
    col.dataframe(pd.DataFrame(top, columns=[label, "Books"]), hide_index=True)
