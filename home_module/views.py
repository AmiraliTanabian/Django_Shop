from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from product_module.models import Product, ProductCategory
from django.db.models import Q
from utils.grouped_list import grouper

class HomeView(TemplateView):
    template_name = "home_module/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_products = Product.objects.filter(is_active=True).order_by("-id")[:12]
        context["latest_products"] = grouper(latest_products, 4)
        return context

class SearchView(View):
    def get(self, request, **kwargs):
        input = self.request.GET.get("input")
        active_products = Product.objects.filter(is_active=True)
        product_result = active_products.filter(Q(name__icontains=input) | Q(brand__title__icontains=input))
        category_result = ProductCategory.objects.filter(is_active=True, title__icontains=input)

        context = {
            "search":input,
            "result":product_result,
            "categories":category_result
        }

        return render(request, "product_module/search.html", context)
