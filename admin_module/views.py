from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, ListView

from contact_module.models import ContactModel
from site_module.models import SiteSetting, SiteBanners, Slider
from .forms import SettingEditForms, BannersEditForm, EditSliderForm


# Create your views here.
def index(request):
    return render(request, "admin_module/index.html")


def main_setting_page(request):
    return render(request, "admin_module/settings/setting_main_page.html")


class MainSetting(View):
    def get(self, request: HttpRequest):
        current_settings = SiteSetting.objects.all().first()
        form = SettingEditForms(instance=current_settings)
        setting = current_settings
        return render(request, "admin_module/settings/settings_page.html", {
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
        return render(request, "admin_module/settings/settings_page.html", {
            "form": form
        })


class SettingsAdsView(LoginRequiredMixin, ListView):
    model = SiteBanners
    paginate_by = 5
    context_object_name = "banners"
    template_name = "admin_module/settings/settings_ads.html"


class AdsEditView(View):
    def get(self, request: HttpRequest, id):
        print("View start")
        current_banner = get_object_or_404(SiteBanners, id=id)
        form = BannersEditForm(instance=current_banner)
        print("View End")

        return render(request, "admin_module/settings/settings_edit_ads.html", {
            "form": form,
            "banner": current_banner,
        })

    def post(self, request: HttpRequest, id):
        current_banner = get_object_or_404(SiteBanners, id=id)
        form = BannersEditForm(request.POST, request.FILES, instance=current_banner)

        if form.is_valid():
            form.save()
            messages.success(request, "بنر با موفقیت تغییر کرده است")
            # return redirect(reverse_lazy('ads_edit_page'))
        return render(request, "admin_module/settings/settings_edit_ads.html", {
            "form": form,
            "banner": current_banner,
        })


class SliderListPage(ListView):
    template_name = "admin_module/settings/settings_sliders_list.html"
    context_object_name = "sliders"
    paginate_by = 5
    model = Slider

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_active=True)
        return query


class SliderDetailView(View):
    def get(self, request: HttpRequest, id):
        current_slider = get_object_or_404(Slider, id=id)
        form = EditSliderForm(instance=current_slider)
        return render(request, "admin_module/settings/settings_slider_edit.html", {
            "form": form,
            "slider": current_slider
        })

    def post(self, request: HttpRequest, id):
        current_slider = get_object_or_404(Slider, id=id)
        form = EditSliderForm(request.POST, request.FILES, instance=current_slider)
        if form.is_valid():
            form.save()
            messages.success(request, "اسلایدر با موفقیت ویرایش شد")
        return render(request, "admin_module/settings/settings_slider_edit.html", {
            "form": form,
            "slider": current_slider
        })


class ContactUsListView(ListView):
    model = ContactModel
    paginate_by = 10
    template_name = "admin_module/contact-us/contact_us_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.order_by("date")
        return query
