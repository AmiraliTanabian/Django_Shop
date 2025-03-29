from django.contrib import admin
from .models import  SiteSetting

class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ["site_name","site_url","is_active"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]

admin.site.register(SiteSetting, SiteSettingAdmin)
