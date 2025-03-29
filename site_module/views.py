from django.shortcuts import render
from .models import SiteSetting

def footer_partial(request):
    site_setting = SiteSetting.objects.filter(is_active=True).first()
    context = {
        "setting":site_setting,
    }
    return render(request, "components/footer_component.html", context)


def header_partial(request):
    site_setting = SiteSetting.objects.filter(is_active=True).first()
    context = {
        "setting":site_setting,
    }
    return render(request, "components/header_component.html", context)
