from django.shortcuts import render
from django.http import HttpRequest


def index_page(request: HttpRequest):
    return render(request, "admin_panel_module/index.html")
