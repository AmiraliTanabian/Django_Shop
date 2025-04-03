from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpRequest
from .forms import EditProfileModelForm
from django.contrib import messages


from phonenumbers import parse, is_valid_number, number_type
from phonenumbers.phonenumberutil import PhoneNumberType

class ProfileDashboardPage(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login_page")
    template_name = "user_profile_module/user_dashboard_page.html"

class EditProfilePageView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login_page")
    def get(self, request: HttpRequest):
        edit_profile_form = EditProfileModelForm(instance=request.user)
        return render(request, "user_profile_module/edit_profile_page.html",
                      {"form":edit_profile_form})

    def post(self, request: HttpRequest):
        edit_profile_form = EditProfileModelForm(request.POST, request.FILES, instance=request.user)

        if edit_profile_form.is_valid():
            mobile = edit_profile_form.cleaned_data["phone_number"]

            if mobile is not None:
                try:
                    parsed_number = parse(mobile, "IR")
                    # mobile_validation = is_valid_number(parsed_number) and number_type(mobile) == PhoneNumberType
                    mobile_validation = is_valid_number(parsed_number)
                except:
                    mobile_validation = False

                # valid phone number
                if mobile_validation:
                    edit_profile_form.save()

                    messages.success(request, "اطلاعات شما ویرایش شد!")
                    return render(request, "user_profile_module/edit_profile_page.html",
                                  {"form": edit_profile_form})

                # invalid phone number
                else:
                    messages.error(request, "تلفن همراه شما نادرست است!")
                    return render(request, "user_profile_module/edit_profile_page.html",
                                  {"form": edit_profile_form})

            # dont have mobile on form
            else:
                edit_profile_form.save()
                messages.success(request, "اطلاعات شما ویرایش شد!")
                return render(request, "user_profile_module/edit_profile_page.html",
                              {"form": edit_profile_form})


        else:
            return render(request, "user_profile_module/edit_profile_page.html",
                          {"form": edit_profile_form})



