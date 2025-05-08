from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_page, name="admin_index_page"),
    path('articles', views.ArticlePageView.as_view(), name="admin_articles_page"),
]
