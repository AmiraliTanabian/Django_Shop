from django.shortcuts import render
from django.views.generic import ListView, DetailView
from news_module.models import Article


class PostListView(ListView):
    template_name = "news_module/post_list.html"
    model = Article
    context_object_name = "news"
    paginate_by = 3

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)


class PostDetailView(DetailView):
    template_name = "news_module/post_details.html"
    context_object_name = "news"
    model = Article
