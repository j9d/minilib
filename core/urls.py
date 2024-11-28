from django.urls import path

from .views import add, home

urlpatterns = [
    path("", home),
    path("add/", add),
]
