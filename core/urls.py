from django.urls import path

from .views import add, home

urlpatterns = [
    path("", home, name="home"),
    path("add/", add, name="add"),
]
