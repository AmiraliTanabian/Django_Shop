from django.views.generic import ListView, DetailView
from news_module.models import Article, ArticleCategories



class PostListView(ListView):
    template_name = "news_module/post_list.html"
    model = Article
    context_object_name = "news"
    paginate_by = 3

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        cats = ArticleCategories.objects.all()
        context["cats"] = cats
        return context

class PostDetailView(DetailView):
    template_name = "news_module/post_details.html"
    context_object_name = "news"
    model = Article
