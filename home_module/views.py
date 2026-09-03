from django.db.models import Q
from django.db.models.aggregates import Count
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from product_module.models import Product, ProductCategory
from utils.grouped_list import grouper


class HomeView(TemplateView):
    template_name = "home_module/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_products = Product.objects.filter(is_active=True).order_by("-id")[:12]
        context["latest_products"] = grouper(latest_products, 4)

        # most popular views
        most_views = Product.objects.filter(is_active=True).annotate(
            view_count=Count('productview')
        ).order_by("-view_count")[:12]
        context["most_views_product"] = grouper(most_views, 4)

        user = self.request.user
        if user.is_authenticated:
            favorite_products = user.favorite_products.all()
        else:
            favorite_products = list()

        context["favorite_list"] = favorite_products

        # Categories part
        cats_list = ProductCategory.objects.filter(is_active=True).order_by("-id")[:7]
        cats_result = []
        for cat in cats_list:
            item = {
                "id": cat.id,
                "title": cat.title,
                "products": list(cat.product_set.all()[:4])
            }
            cats_result.append(item)

        context["cats_result"] = cats_result

        # Best-selling part
        best_selling_products = Product.objects.filter(is_active=True).order_by("-order_count")[:12]
        best_selling_products = grouper(best_selling_products, 4)
        context["best_shellings"] = best_selling_products

        return context


class SearchView(View):
    def get(self, request, **kwargs):
        input = self.request.GET.get("input")
        active_products = Product.objects.filter(is_active=True)
        product_result = active_products.filter(Q(name__icontains=input) | Q(brand__title__icontains=input))
        category_result = ProductCategory.objects.filter(is_active=True, title__icontains=input)

        context = {
            "search": input,
            "result": product_result,
            "categories": category_result
        }

        return render(request, "product_module/search.html", context)
