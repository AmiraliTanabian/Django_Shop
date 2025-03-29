from django.contrib import admin
from .models import ContactModel

class ContactModelAdmin(admin.ModelAdmin):
    list_display = ["subject", "email", "is_read"]
    list_filter = ["is_read"]
    list_editable = ["is_read"]


admin.site.register(ContactModel, ContactModelAdmin)