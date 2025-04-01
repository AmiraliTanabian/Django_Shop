from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from . import forms
from django.urls import reverse_lazy
from . import models
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest


class loginView(FormView):
    form_class = forms.loginForm
    success_url = reverse_lazy("home_page")
    template_name = "auth_module/login_page.html"

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        is_authenticate = authenticate(self.request, username=username, password=password)

        if is_authenticate:
            login(self.request, is_authenticate)
            return redirect(reverse_lazy("home_page"))

        else:
            messages.error(self.request, "نام کاربری یا رمز عبور شما نادرست است")
            return render(self.request, "auth_module/login_page.html",
                          {"form":form})


class registerView(View):
    def get(self, request):
        return render(request, "auth_module/register_account.html")

class logoutView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login_page")
    def get(self, request: HttpRequest):
        username = request.user.username
        logout(request)
        msg = f"""
        کاربر {username}
        شما با موفقیت خارج شدید.
        از اینکه وقت خود را در سایت ما گذراندید ممنونیم :)
        """
        messages.success(request, msg)
        return redirect("home_page")
