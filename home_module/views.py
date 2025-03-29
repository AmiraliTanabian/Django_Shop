from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "home_module/home.html"
