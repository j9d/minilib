from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=64)


class Book(models.Model):
    isbn = models.CharField(max_length=13)
    key = models.CharField(max_length=64)
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author)
    year = models.PositiveIntegerField(null=True, blank=True)
