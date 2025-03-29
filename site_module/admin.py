from django.contrib import admin
from .models import  SiteSetting, Slider

class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ["site_name","site_url","is_active"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]

class SliderAdmin(admin.ModelAdmin):
    list_display = ["title", "url" ,"banner", "is_active"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]


admin.site.register(SiteSetting, SiteSettingAdmin)
admin.site.register(Slider, SliderAdmin)
