from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from . import forms
from django.urls import reverse_lazy
from . import models
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, Http404
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.hashers import make_password

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
                          {"form":form})


class registerView(View):
    def get(self, request):
        form = forms.registerForm()
        if not request.user.is_authenticated:
            return render(request, "auth_module/register_account.html",
                          {"form":form})
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
            elif models.TempUser.objects.filter(Q(username=username) | Q(password=password)).exists():
                form.add_error("username",
        "شما قبلا با این ایمیل یا نام کاربری درخواست ثبت حساب دادید.\nلطفا به ایمیل خود بروید و حساب را فعال کنید")

            else:
                # Create temp user
                random_string = get_random_string(72)
                models.TempUser.objects.create(
                    username = username,
                    email = email,
                    password = make_password(password),
                    random_string = random_string
                )

                # Send mail to set user account activate
                verification_url = reverse_lazy("verify_account", args=[random_string])
                body_context = {
                    "verification_url" : settings.SITE_URL + verification_url
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
                          {"form":form})


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
        temp_user = models.TempUser.objects.filter(random_string=random_string).first()


        if not temp_user:
            raise Http404

        # 12 * 3600 = 12h
        elif timezone.now().timestamp() - temp_user.date.timestamp() > 12 * 3600:
            context = {"status":"timeEnd"}
            temp_user.delete()


        else:
            context = {"status":"Ok"}
            username = temp_user.username
            password = temp_user.password
            email = temp_user.email
            temp_user.delete()

            UserObject = user_model(username=username, password=password, email=email)
            UserObject.save()


        return render(request, "auth_module/verify_result.html", context)
