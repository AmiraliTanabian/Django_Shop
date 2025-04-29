from django.urls import path

from . import views

urlpatterns = [
    path("", views.OrderPage.as_view(), name="order_page"),
    path("add-to-order", views.AddProductToOrder.as_view(), name="add_product_to_order"),
    path("remove-from-order", views.RemoveFromOrder.as_view(), name="remove_order"),
    path("add-product-count", views.AddProductCountView.as_view(), name="add_product_count"),
    path("remove-product-count", views.RemoveProductCountView.as_view(), name="remove_product_count"),
    # path('request', views.payment_request, name='request-payment'),
    # path('verify', views.payment_verify, name='verify-payment'),
]
