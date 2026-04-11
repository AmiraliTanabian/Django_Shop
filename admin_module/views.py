from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "admin_module/index.html")


def setting_page(request):
    return render(request, "admin_module/setting_main_page.html")
