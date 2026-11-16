import json
from pathlib import Path

import pandas as pd

import requests

URL = "https://openlibrary.org/"
LIMIT = 3
BOOKS_CSV = "data/books.csv"
OUTPUT_JSON = "data/descriptions/descriptions.json"
FIELDS = {
    "description": "description",
    "subjects": "subjects",
    "places": "subject_places",
    "times": "subject_times",
}


def fetch(url, **params):
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as e:
        print(f"Request failed for {url}: {e}")
        return {}


def get_data(book_name):
    docs = fetch(URL + "search.json", q=book_name, limit=LIMIT).get("docs", [])
    data = dict.fromkeys(FIELDS)

    # fill each missing field from the next search result until all are found
    for doc in docs:
        work = fetch(URL + doc["key"] + ".json")
        for field, key in FIELDS.items():
            data[field] = data[field] or work.get(key)
        if all(data.values()):
            break

    # description is sometimes a plain string, sometimes {"type": ..., "value": ...}
    if isinstance(data["description"], dict):
        data["description"] = data["description"].get("value")

    return {field: value or None for field, value in data.items()}


def book_info(csv_path=BOOKS_CSV):
    books = pd.read_csv(csv_path)
    titles = [row["title"] for idx, row in books.iterrows()]
    return {title: get_data(title) for title in titles}


if __name__ == "__main__":
    output = Path(OUTPUT_JSON)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(book_info(), indent=2))
