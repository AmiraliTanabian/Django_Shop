from django.shortcuts import render
from django.views import View

class loginView(View):
    def get(self, request):
        return render(request, "auth_module/login_page.html")

class registerView(View):
    def get(self, request):
        return render(request, "auth_module/register_account.html")