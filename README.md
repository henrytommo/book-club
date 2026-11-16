# book-club

streamlit dashboard using the openlibrary api (https://openlibrary.org/developers/api) to get stats for book club.

get_data can be used to get the data for an input csv of books. for batch processing, a dict of book data can be saved to the data/ folder as a py file. will update this to make more flexible.

aim is to use a small embeddings model on the various metadata from openlibrary (mainly the "description" field) to see if there are any types of books we tend to read more. we've only read 25 books so not nearly enough to fine tune.