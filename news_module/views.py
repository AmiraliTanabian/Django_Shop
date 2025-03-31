from django.views.generic import ListView, DetailView
from news_module.models import Article, ArticleCategories, ArticleTag
from django.db.models.aggregates import Min, Max



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


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        stats = self.model.objects.aggregate(Max("id"), Min("id"))
        context["max_id"] = stats["id__max"]
        context["min_id"] = stats["id__min"]

        cats = ArticleCategories.objects.all()
        context["cats"] = cats

        current_post = Article.objects.get(id=self.kwargs['pk'])
        current_cats = current_post.categories.all()
        context["current_cats"] = current_cats

        return context

class CategoryPageView(ListView):
    template_name = "news_module/category_blog_page.html"
    model = Article
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        slug = self.kwargs["slug"]
        query = self.model.objects.filter(is_active=True)
        ok_items = []
        for item in query :
            for cat in item.categories.all():
                if cat.slug == slug :
                    ok_items.append(item)
                    break
        return ok_items

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        cat_title = ArticleCategories.objects.get(slug=self.kwargs["slug"]).title
        context["cat_title"] = cat_title

        cats = ArticleCategories.objects.all()
        context["cats"] = cats

        return context

class TagPageView(ListView):
    template_name = "news_module/tag_blog_page.html"
    model = Article
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        slug = self.kwargs["slug"]
        query = self.model.objects.filter(is_active=True)
        ok_items = []
        for item in query:
            for tag in item.tags.all():
                if tag.slug == slug:
                    ok_items.append(item)
                    break
        return ok_items

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        tag_title = ArticleTag.objects.get(slug=self.kwargs["slug"]).tag_name
        context["tag_title"] = tag_title

        cats = ArticleCategories.objects.all()
        context["cats"] = cats

        return context
