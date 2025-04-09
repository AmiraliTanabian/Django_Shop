from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import TempUser


class TempUserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "date"]


admin.site.register(get_user_model())
admin.site.register(TempUser, TempUserAdmin)
