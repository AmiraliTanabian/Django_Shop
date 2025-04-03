from django.urls import path
from .views import ProductPageView, ProductDetailView, ProductCategoryPageView


urlpatterns = [
    path("", ProductPageView.as_view(), name="product_page"),
    path("<int:pk>", ProductDetailView.as_view(), name="product_detail"),
    path("category/<slug:slug>", ProductCategoryPageView.as_view(), name="product_category_page")
]