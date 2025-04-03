from django.views.generic import ListView, DetailView
from .models import Product, ProductCategory
from django.shortcuts import render


class ProductPageView(ListView):
    template_name = "product_module/product_list.html"
    model = Product
    context_object_name = "products"
    paginate_by = 5

class ProductDetailView(DetailView):
    template_name = "product_module/product_detail.html"
    model = Product

class ProductCategoryPageView(ListView):
    template_name = "product_module/product_category_page.html"
    model = Product
    context_object_name = "products"
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
        cat_title = ProductCategory.objects.get(slug=self.kwargs["slug"]).title
        context["cat_title"] = cat_title

        return context

def product_category_part_partial(request):
    cats = ProductCategory.objects.filter(is_active=True, parent=None).prefetch_related("childs")
    context = {
        "cats" : cats
    }
    return render(request, "product_module/components/product_category_component.html", context)
