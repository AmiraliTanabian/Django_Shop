from django.contrib import admin

from .models import ticket_model, ticket_attachment

admin.site.register(ticket_model)
admin.site.register(ticket_attachment)
