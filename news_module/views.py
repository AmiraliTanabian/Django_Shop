from django.shortcuts import render
from django.views.generic import ListView
from news_module.models import Article


class NewsListView(ListView):
    template_name = "news_module/news_list.html"
    model = Article
    context_object_name = "news"