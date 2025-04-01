from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import TempUser

class TempUserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "data"]


admin.site.register(get_user_model())
admin.site.register(TempUser, TempUserAdmin)