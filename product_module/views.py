from django.shortcuts import (render)
from django.views.generic import ListView, DetailView
from .models import Product

class ProductPageView(ListView):
    template_name = "product_module/product_list.html"
    model = Product
    context_object_name = "products"
    # paginate_by = 5


class ProductDetailView(DetailView):
    template_name = "product_module/product_detail.html"
    model = Product
