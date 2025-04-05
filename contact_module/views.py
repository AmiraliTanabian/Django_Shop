from django.shortcuts import render, redirect
from django.views import View
from .forms import ContactUsForm
from site_module.models import SiteSetting, SiteBanners
from django.contrib import messages

class ContactView(View):
    def get(self, request):
        site_setting = SiteSetting.objects.filter(is_active=True).first()
        banners = SiteBanners.objects.filter(is_active=True, position=SiteBanners.PositionChoices.contact)
        context = {
            "setting": site_setting,
            "form" : ContactUsForm(),
            "banners" : banners,
        }
        return render(request, "contact_module/contact_us.html", context)

    def post(self, request):
        site_setting = SiteSetting.objects.filter(is_active=True).first()
        form = ContactUsForm(data=request.POST)

        if not form.is_valid():
            context = {
                "setting": site_setting,
                "form" : form
            }
            return render(request, "contact_module/contact_us.html", context)

        else:
            form.save()

            messages.success(request, "پیام شما با موفقیت ارسال شد \n نتیجه آن را از طریق ایمیل دریافت میکنید!")
            return redirect("home_page")
