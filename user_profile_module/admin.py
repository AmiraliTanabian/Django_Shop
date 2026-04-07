from django.contrib import admin

from .models import ticket_model, ticket_attachment, TicketAnswerModel


class TicketAnswerAdmin(admin.ModelAdmin):
    fields = ["text", "ticket"]


admin.site.register(ticket_model, TicketAnswerAdmin)
admin.site.register(ticket_attachment)
admin.site.register(TicketAnswerModel)
