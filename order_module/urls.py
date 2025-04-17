from django.urls import path

from . import views

urlpatterns = [
    path("", views.OrderPage.as_view(), name="order_page"),
    path("add-to-order", views.AddProductToOrder.as_view(), name="add_product_to_order"),
    path("remove-from-order", views.RemoveFromOrder.as_view(), name="remove_order")
]
