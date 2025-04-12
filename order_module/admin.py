from django.contrib import admin

from .models import orderModel, orderProductModel


class orderAdmin(admin.ModelAdmin):
    list_display = ["user", "paid_date", "is_paid"]
    list_filter = ["user", "is_paid"]


class orderProductAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "count", "finally_price"]
    list_filter = ["order"]


admin.site.register(orderModel, orderAdmin)
admin.site.register(orderProductModel, orderProductAdmin)
