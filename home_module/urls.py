from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home_page"),
    path("search", views.SearchView.as_view(), name="search_product_page"),
]
