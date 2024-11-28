from typing import Any

import requests

API_URL = "https://openlibrary.org/search.json"


def search(isbn: str):
    response = requests.get(f"{API_URL}/?isbn={isbn}")

    if not response.ok:
        return None

    data: dict[str, Any] = response.json()

    if data["numFound"] == 0:
        return None

    book: dict[str, Any] = data["docs"][0]
    return book
