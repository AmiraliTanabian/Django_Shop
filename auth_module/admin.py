from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import TempUser


class TempUserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "date"]


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"),
         {"fields": ("first_name", "last_name", "email", "about_user", "profile_image", "phone_number", "address")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(TempUser, TempUserAdmin)
