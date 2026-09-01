from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, ListView

from site_module.models import SiteSetting, SiteBanners
from .forms import SettingEditForms, BannersEditForm


# Create your views here.
def index(request):
    return render(request, "admin_module/index.html")


def main_setting_page(request):
    return render(request, "admin_module/setting_main_page.html")


class MainSetting(View):
    def get(self, request: HttpRequest):
        current_settings = SiteSetting.objects.all().first()
        form = SettingEditForms(instance=current_settings)
        setting = current_settings
        return render(request, "admin_module/settings_page.html", {
            "form": form,
            "setting": setting,
        })

    def post(self, request: HttpRequest):
        current_settings = SiteSetting.objects.all().first()
        form: SettingEditForms = SettingEditForms(request.POST, request.FILES, instance=current_settings)

        if form.is_valid():
            form.save()
            messages.success(request, "اطلاعات با موفقیت تغییر کرده است")
            return redirect(reverse_lazy('admin_setting_main_page'))
        return render(request, "admin_module/settings_page.html", {
            "form": form
        })


class SettingsAdsView(LoginRequiredMixin, ListView):
    model = SiteBanners
    paginate_by = 1
    context_object_name = "banners"
    template_name = "admin_module/settings_ads.html"


class AdsEditView(View):
    def get(self, request: HttpRequest, id):
        current_banner = get_object_or_404(SiteBanners, id=int(id))
        form = BannersEditForm(instance=current_banner)
        return render(request, "admin_module/edit_ads.html", {
            "form": form,
            "banner": current_banner,
        })

    def post(self, request: HttpRequest, id):
        current_banner = get_object_or_404(SiteBanners, id=id)
        form = BannersEditForm(request.POST, request.FILES, instance=current_banner)

        if form.is_valid():
            form.save()
            messages.success(request, "بنر با موفقیت تغییر کرده است")
            return redirect(reverse_lazy('ads_edit_page_page'))
        return render(request, "admin_module/edit_ads.html", {
            "form": form
        })
