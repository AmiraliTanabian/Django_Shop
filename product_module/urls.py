from django.urls import path
from .views import ProductPageView, ProductDetailView


urlpatterns = [
    path("", ProductPageView.as_view(), name="product_page"),
    path("<int:pk>", ProductDetailView.as_view(), name="product_detail")
]