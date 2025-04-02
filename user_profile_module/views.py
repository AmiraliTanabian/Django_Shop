from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class ProfileDashboardPage(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login_page")
    template_name = "user_profile_module/user_dashboard_page.html"
