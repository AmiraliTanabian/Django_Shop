from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View

from site_module.models import SiteSetting
from .forms import SettingEditForms


# Create your views here.
def index(request):
    return render(request, "admin_module/index.html")


def main_setting_page(request):
    return render(request, "admin_module/setting_main_page.html")


class MainSetting(View):
    def get(self, request: HttpRequest):
        current_settings = SiteSetting.objects.all().first()
        form = SettingEditForms(instance=current_settings)
        return render(request, "admin_module/settings_page.html", {
            "form": form
        })

    def post(self, request: HttpRequest):
        current_settings = SiteSetting.objects.all().first()
        form: SettingEditForms = SettingEditForms(request.POST, request.FILES, instance=current_settings)

        if form.is_valid():
            form.save()
            messages.success(request, "اطلاعات با موفقیت تغییر کرده است")
            print("Form is valid")
            return redirect(reverse_lazy('admin_setting_page'))
        print("form is invalid")
        print(form.errors)
        return render(request, "admin_module/settings_page.html", {
            "form": form
        })
