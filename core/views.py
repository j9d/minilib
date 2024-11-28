from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseNotAllowed
from django.http.response import HttpResponse
from django.template.response import TemplateResponse


@login_required
def home(request: HttpRequest):
    return TemplateResponse(request, "home.html")


@login_required
def add(request: HttpRequest):
    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=["POST"])

    return HttpResponse()
