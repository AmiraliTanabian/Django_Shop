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

def product_category_part_partial(request):
    cats = ProductCategory.objects.filter(is_active=True, parent=None).prefetch_related("childs")
    context = {
        "cats" : cats
    }
    return render(request, "product_module/components/product_category_component.html", context)