from django.urls import path

from . import views

urlpatterns = [
    path("add-to-order", views.AddProductToOrder.as_view(), name="add_product_to_order"),
]
