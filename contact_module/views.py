from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from site_module.models import SiteSetting, SiteBanners
from .forms import ContactUsForm


class ContactView(View):
    def get(self, request):
        banners = SiteBanners.objects.filter(is_active=True, position=SiteBanners.PositionChoices.contact)
        site_setting = SiteSetting.objects.filter(is_active=True).first()
        context = {
            "setting": site_setting,
            "form": ContactUsForm(),
            "banners": banners,
        }
        return render(request, "contact_module/contact_us.html", context)

    def post(self, request):
        banners = SiteBanners.objects.filter(is_active=True, position=SiteBanners.PositionChoices.contact)
        site_setting = SiteSetting.objects.filter(is_active=True).first()
        form = ContactUsForm(data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "پیام شما با موفقیت ارسال شد \n نتیجه با ایمیل برای شما ارسال میشود")
            return redirect(reverse_lazy("home_page"))

        print("form is invalid ")
        print(form.errors)

        context = {
            "setting": site_setting,
            "form": form,
            "banners": banners,
        }
        return render(request, "contact_module/contact_us.html", context)
