from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse


@login_required
def home(request):
    return TemplateResponse(request, "home.html")
