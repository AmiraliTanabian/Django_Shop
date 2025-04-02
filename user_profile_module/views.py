from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpRequest
from .forms import EditProfileModelForm

class ProfileDashboardPage(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login_page")
    template_name = "user_profile_module/user_dashboard_page.html"

class EditProfilePageView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login_page")
    def get(self, request: HttpRequest):
        edit_profile_form = EditProfileModelForm
        return render(request, "user_profile_module/edit_profile_page.html",
                      {"form":edit_profile_form})

