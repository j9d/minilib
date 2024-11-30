from typing import Any

from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
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
    books: list[dict[str, Any]] = []
    queryset = Book.objects.all().order_by("title").prefetch_related("authors")
    for book in queryset:
        book_dict = model_to_dict(book, fields=["title", "year", "authors"])
        authors = book.authors.values_list("name", flat=True)
        book_dict["authors"] = authors
        books.append(book_dict)

    context = {
        "books": books,
    }
    return TemplateResponse(
        request,
        template="home.html",
        context=context,
    )


@login_required
def add(request: HttpRequest):
    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=["POST"])

    isbn = request.POST.get("isbn", None)
    if not isbn:
        return HttpResponseBadRequest("ISBN is required")

    if Book.objects.filter(isbn=isbn).exists():
        return HttpResponse("Book already exists", status=200)

    book = search(isbn)
    if book is None:
        return HttpResponseNotFound("ISBN not found")

    author_keys: list[str] = book.get("author_key", [])
    author_names: list[str] = book.get("author_name", [])

    authors: list[Author] = []
    for key, name in zip(author_keys, author_names):
        existing_author = Author.objects.filter(key=key).first()
        if existing_author:
            authors.append(existing_author)
        else:
            authors.append(Author.objects.create(key=key, name=name))

    publish_years: list[int] = book.get("publish_year", [])
    year: int | None = None
    if publish_years:
        year = min(publish_years)

    title: str = book.get("title", "")
    key: str = book.get("key", "")

    book = Book.objects.create(
        isbn=isbn,
        key=key,
        title=title,
        year=year,
    )
    for author in authors:
        book.authors.add(author)

    return HttpResponse(
        f"Book '{title}' added successfully",
        status=201,
    )
