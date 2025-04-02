from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="news_page"),
    path("<int:pk>", views.PostDetailView.as_view(), name="post_detail_page"),
    path("cat/<slug:slug>", views.CategoryPageView.as_view(), name="category_blog_page"),
    path("tag/<slug:slug>", views.TagPageView.as_view(), name="tag_blog_page"),
    path("add_comment", views.add_article_comment, name="add_article_comment")
]