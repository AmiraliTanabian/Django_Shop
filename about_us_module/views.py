from django.shortcuts import render
from site_module.models import SiteSetting
from django.views import View

class AboutView(View):
    def get(self, request):
        setting = SiteSetting.objects.filter(is_active=True).first()
        context = {
            "setting":setting
        }
        return render(request, "about_us_module/about_us.html", context)