from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from phonenumbers import parse, is_valid_number

from order_module.models import orderModel
from .forms import EditProfileModelForm, EditPasswordForm


class ProfileDashboardPage(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login_page")
    template_name = "user_profile_module/user_dashboard_page.html"


class EditProfilePageView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login_page")

    def get(self, request: HttpRequest):
        edit_profile_form = EditProfileModelForm(instance=request.user)
        return render(request, "user_profile_module/edit_profile_page.html",
                      {"form": edit_profile_form})

    def post(self, request: HttpRequest):
        edit_profile_form = EditProfileModelForm(request.POST, request.FILES, instance=request.user)

        if edit_profile_form.is_valid():
            mobile = edit_profile_form.cleaned_data["phone_number"]
            email = edit_profile_form.cleaned_data["email"].strip()

            # mobile validation
            if mobile is not None:
                try:
                    parsed_number = parse(mobile, "IR")
                    mobile_validation = is_valid_number(parsed_number)
                except:
                    mobile_validation = False

                # Second step for mobile validation
                mobile_exists = get_user_model().objects.filter(phone_number=mobile)
                if mobile_exists and mobile_exists == request.user:
                    mobile_validation = False

            # dont have mobile
            else:
                messages.error(request, "فیلد موبایل ضرروری مبیاشد")
                return render(request, "user_profile_module/edit_profile_page.html",
                              {"form": edit_profile_form})

            # email validation
            if email != '':
                email_exists = get_user_model().objects.filter(email=email).first()
                if email_exists and email_exists != request.user:
                    email_validation = False
                else:
                    email_validation = True

            # dont have email
            else:
                messages.error(request, "فیلد ایمیل ضرروری مبیاشد")
                return render(request, "user_profile_module/edit_profile_page.html",
                              {"form": edit_profile_form})

            if email_validation and mobile_validation:
                edit_profile_form.save()
                messages.success(request, "اطلاعات شما ویرایش شد")
                return render(request, "user_profile_module/edit_profile_page.html",
                              {"form": edit_profile_form})

            elif not email_validation:
                messages.error(request, "این ایمیل قبلا ثبت شده :(")
                return render(request, "user_profile_module/edit_profile_page.html",
                              {"form": edit_profile_form})

            # invalid phone number
            else:
                messages.error(request, "متاسفانه موبایل شما نادرست است :(")
                return render(request, "user_profile_module/edit_profile_page.html",
                              {"form": edit_profile_form})

        # form is invalid
        else:
            return render(request, "user_profile_module/edit_profile_page.html",
                          {"form": edit_profile_form})


class EditPasswordPageView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login_page")

    def get(self, request):
        form = EditPasswordForm
        return render(request, "user_profile_module/edit_password_page.html", {"form": form})

    def post(self, request):
        form = EditPasswordForm(request.POST)

        if form.is_valid():
            user = get_user_model().objects.get(id=request.user.id)
            old_password = form.cleaned_data.get("password")
            new_password = form.cleaned_data.get("new_password")
            is_password_correct = check_password(old_password, user.password)

            if is_password_correct:
                user.set_password(new_password)
                user.save()
                messages.success(request, "رمز عبور شما با موفقیت تغییر کرد")
                return render(request, "user_profile_module/edit_password_page.html", {"form": form})

            else:
                messages.error(request, "رمز عبور شما با نادرست است.")
                return render(request, "user_profile_module/edit_password_page.html", {"form": form})

        else:
            return render(request, "user_profile_module/edit_password_page.html", {"form": form})


class ProfileFavoriteProductsView(LoginRequiredMixin, ListView):
    template_name = "user_profile_module/favorite_list_on_profile.html"
    context_object_name = "products"
    login_url = reverse_lazy("login_page")
    model = get_user_model()
    paginate_by = 5

    def get_queryset(self):
        user_id = self.request.user.id
        query = get_user_model().objects.get(id=user_id)
        query = query.favorite_products.all()
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        favorite_products = user.favorite_products.all()
        context["favorite_list"] = favorite_products
        return context


class ProfileOrders(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("login_page")
    template_name = "user_profile_module/user_orders_list.html"
    model = orderModel
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_paid=True, user=self.request.user)

        return query


class orderPageView(LoginRequiredMixin, DetailView):
    template_name = "user_profile_module/order_detail.html"
    context_object_name = "order"
    model = orderModel

    def get_queryset(self):
        query = super().get_queryset()
        query.filter(user=self.request.user).prefetch_related("orderproductmodel_set")
        return query
