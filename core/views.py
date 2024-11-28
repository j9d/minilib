from typing import Any

from django.contrib.auth.decorators import login_required
from django.http import (
    HttpRequest,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    HttpResponseNotFound,
)
from django.http.response import HttpResponse
from django.template.response import TemplateResponse

from core.models import Author, Book
from core.utils import search


@login_required
def home(request: HttpRequest):
    return TemplateResponse(request, "home.html")


@login_required
def add(request: HttpRequest):
    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=["POST"])

    isbn = request.POST.get("isbn", None)
    if isbn is None:
        return HttpResponseBadRequest("ISBN is required")

    if Book.objects.filter(isbn=isbn).exists():
        return HttpResponse(status=200)

    book = search(isbn)
    if book is None:
        return HttpResponseNotFound()

    book_info: dict[str, Any] = book.get("docs", [])[0]

    author_keys: list[str] = book_info.get("author_key", [])
    author_names: list[str] = book_info.get("author_name", [])

    authors: list[Author] = []
    for key, name in zip(author_keys, author_names):
        existing_author = Author.objects.filter(author_key=key).first()
        if existing_author:
            authors.append(existing_author)
        else:
            authors.append(Author.objects.create(author_key=key, name=name))

    publish_years: list[int] = book_info.get("publish_year", [])
    year: int | None = None
    if publish_years:
        year = min(publish_years)

    title: str = book_info.get("title", "")
    key: str = book_info.get("key", "")

    book = Book.objects.create(
        isbn=isbn,
        key=key,
        title=title,
        year=year,
    )
    for author in authors:
        book.authors.add(author)

    return HttpResponse(status=201)
