from django.shortcuts import render
from .models import SiteSetting, Slider

def footer_partial(request):
    site_setting = SiteSetting.objects.filter(is_active=True).first()
    context = {
        "setting":site_setting,
    }
    return render(request, "components/footer_component.html", context)


def header_partial(request):
    print(request.path)
    site_setting = SiteSetting.objects.filter(is_active=True).first()
    context = {
        "setting":site_setting,
        "path": request.path,
    }
    return render(request, "components/header_component.html", context)


def slider_partial(request):
    sliders = Slider.objects.filter(is_active=True)
    context = {
        "sliders":sliders,
    }
    return render(request, "components/slider.html", context)