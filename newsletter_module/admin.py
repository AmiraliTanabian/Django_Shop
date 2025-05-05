from django.contrib import admin

from . import models


class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ["email", "is_active"]
    list_filter = ["is_active"]
    list_editable = ["is_active"]


admin.site.register(models.newsLetterModel, NewsLetterAdmin)
