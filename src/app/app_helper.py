from collections import Counter

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
