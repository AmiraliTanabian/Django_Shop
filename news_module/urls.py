from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="news_page"),
    path("<int:pk>", views.PostDetailView.as_view(), name="post_detail_page")
]