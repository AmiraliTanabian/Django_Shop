from django.urls import path
from .views import ProductPageView, ProductDetailView, ProductCategoryPageView, ProductBrandPage, AddProductToFavoriteView

urlpatterns = [
    path("", ProductPageView.as_view(), name="product_page"),
    path("<int:pk>", ProductDetailView.as_view(), name="product_detail"),
    path("category/<slug:slug>", ProductCategoryPageView.as_view(), name="product_category_page"),
    path("brand/<slug:slug>", ProductBrandPage.as_view(), name="product_brand_page"),
    path("add-to-favorite", AddProductToFavoriteView.as_view(), name="add_product_to_favorite")
]