from django.urls import path

from .views import (ProductPageView, ProductDetailView, ProductBrandPage,
                    AddProductToFavoriteView,
                    FavoriteProductsView, RemoveFromFavoriteView, ProductTagView, ProductPriceFilter)

urlpatterns = [
    path("", ProductPageView.as_view(), name="product_page"),
    path("<int:pk>", ProductDetailView.as_view(), name="product_detail"),
    path("category/<slug:slug>", ProductPageView.as_view(), name="product_category_page"),
    path("brand/<slug:slug>", ProductBrandPage.as_view(), name="product_brand_page"),
    path("add-to-favorite", AddProductToFavoriteView.as_view(), name="add_product_to_favorite"),
    path("favorite-list", FavoriteProductsView.as_view(), name="favorite_list"),
    path("remove-from-favorite", RemoveFromFavoriteView.as_view(), name="remove_from_favorite"),
    path("tag/<slug:slug>", ProductTagView.as_view(), name="product_tag_page"),
    path("price-fiter", ProductPriceFilter.as_view(), name="product_price_filter")
]
