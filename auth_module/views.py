from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import FormView

from . import forms

user_model = get_user_model()


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
                          {"form": form})


class registerView(View):
    def get(self, request):
        form = forms.registerForm()
        if not request.user.is_authenticated:
            return render(request, "auth_module/register_account.html",
                          {"form": form})
        else:
            return redirect(reverse_lazy("home_page"))

    def post(self, request):
        form = forms.registerForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            username = form.cleaned_data['username']
            password = form.cleaned_data["password"]

            if user_model.objects.filter(email=email).exists():
                form.add_error("email", "ایمیل شما قبلا ثبت شده است :(")

            elif user_model.objects.filter(username=username).exists():
                form.add_error("username", "متاسفانه نام کاربری شما قبلا ثبت شده است :(")

            # The user has not previously requested an account registration
            elif user_model.objects.filter(username=username, password=password, account_activated=False).exists():
                form.add_error("username",
                               "شما قبلا با این ایمیل یا نام کاربری درخواست ثبت حساب دادید.\nلطفا به ایمیل خود بروید و حساب را فعال کنید")

            else:
                active_code = get_random_string(72)
                user_model.objects.create(
                    username=username,
                    email=email,
                    password=make_password(password),
                    active_code=active_code,
                    active_code_sent_date=datetime.now(),
                )

                # Send mail to set user account activate
                verification_url = reverse_lazy("verify_account", args=[active_code])
                body_context = {
                    "verification_url": settings.SITE_URL + verification_url
                }
                body = render_to_string("auth_module/email_activate_template.html", body_context)
                msg = EmailMessage(
                    "فعالسازی حساب کاربری",
                    body,
                    "atanabain@gmail.com",
                    [email]
                )
                msg.content_subtype = "html"
                msg.send()

                # Send success msg and show form
                messages.success(request,
                                 "ایمیل فعال سازی حساب برای شما ارسال شد\n لطفا ایمیل خود را چک کنید")

            return render(request, "auth_module/register_account.html",
                          {"form": form})


        else:
            return render(request, "auth_module/register_account.html",
                          {"form": form})


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


class verifyAccount(View):
    def get(self, request, random_string):
        user = get_object_or_404(get_user_model(), active_code=random_string, account_activated=False)

        # 12 * 3600 = 12h
        if timezone.now().timestamp() - user.active_code_sent_date.timestamp() > 12 * 3600:
            context = {"status": "timeEnd"}
            user.delete()


        else:
            context = {"status": "Ok"}
            user.account_activated = True
            new_random_string = get_random_string(72)
            user.active_code = new_random_string
            user.active_code_sent_date = datetime.now()
            user.save()

        return render(request, "auth_module/verify_result.html", context)
