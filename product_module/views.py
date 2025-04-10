from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView

from site_module.models import SiteBanners
from utils.http_service import get_user_ip
from .models import Product, ProductCategory, Brand, ProductView, ProductGallery
from utils.grouped_list import grouper


class ProductPageView(ListView):
    template_name = "product_module/product_list.html"
    model = Product
    context_object_name = "products"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            favorite_products = user.favorite_products.all()
        else:
            favorite_products = list()

        context["favorite_list"] = favorite_products
        context["banners"] = SiteBanners.objects.filter(is_active=True, position=SiteBanners.PositionChoices.product)
        return context


class ProductDetailView(DetailView):
    template_name = "product_module/product_detail.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["banners"] = SiteBanners.objects.filter(is_active=True,
                                                        position=SiteBanners.PositionChoices.product_detail)

        # Set view for product
        user_ip = get_user_ip(self.request)
        has_been_visited = ProductView.objects.filter(product=self.object, ip=user_ip).exists()

        user = None
        if self.request.user.is_authenticated:
            user = self.request.user

        if not has_been_visited:
            new_visit = ProductView(product=self.object, ip=get_user_ip(self.request), user=user)
            new_visit.save()

        # Product Gallery
        product_gallery = list(ProductGallery.objects.filter(is_active=True, product=self.object))
        product_gallery.append(self.object)
        context["product_gallery"] = grouper(product_gallery, 3)

        return context


class ProductBrandPage(ListView):
    template_name = "product_module/product_brand_page.html"
    context_object_name = "products"
    model = Product

    def get_queryset(self):
        base_query = self.model.objects.filter(is_active=True)
        brand_slug = self.kwargs["slug"]
        query = base_query.filter(brand__slug=brand_slug)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand_name = Brand.objects.filter(slug=self.kwargs["slug"]).first().title
        context["brand_name"] = brand_name

        user = self.request.user
        favorite_products = user.favorite_products.all()
        context["favorite_list"] = favorite_products

        return context


class ProductCategoryPageView(ListView):
    template_name = "product_module/product_category_page.html"
    model = Product
    context_object_name = "products"
    paginate_by = 5

    def get_queryset(self):
        slug = self.kwargs["slug"]
        query = self.model.objects.filter(is_active=True)
        ok_items = []
        for item in query:
            for cat in item.categories.all():
                if cat.slug == slug:
                    ok_items.append(item)
                    break
        return ok_items

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        cat_title = ProductCategory.objects.get(slug=self.kwargs["slug"]).title
        context["cat_title"] = cat_title

        user = self.request.user
        favorite_products = user.favorite_products.all()
        context["favorite_list"] = favorite_products

        return context


class AddProductToFavoriteView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            if "product_id" in request.GET:
                user_id = request.user.id
                user = get_user_model().objects.get(id=user_id)
                product = Product.objects.get(id=request.GET["product_id"])
                product.is_favorite = True
                user.favorite_products.add(product)

                return HttpResponse("Product added to favorite")
            return HttpResponse("Product id not found error!")

        else:
            return HttpResponse("User login error!!")


class FavoriteProductsView(LoginRequiredMixin, ListView):
    template_name = "product_module/favorite_list.html"
    context_object_name = "products"
    login_url = reverse_lazy("login_page")
    model = get_user_model()
    paginate_by = 5

    def get_queryset(self):
        user_id = self.request.user.id
        query = get_user_model().objects.get(id=user_id)
        query = query.favorite_products.all()
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        favorite_products = user.favorite_products.all()
        context["favorite_list"] = favorite_products
        return context


def product_category_part_partial(request):
    cats = ProductCategory.objects.filter(is_active=True, parent=None).prefetch_related("childs")
    context = {
        "cats": cats
    }
    return render(request, "product_module/components/product_category_component.html", context)


def product_brand_partial(request):
    brands = Brand.objects.filter(is_active=True)
    context = {
        "brands": brands,
    }
    return render(request, "product_module/components/brand_list_component.html", context)


def product_price_filter_partial(request):
    return render(request, "product_module/components/product_price_component.html")


class RemoveFromFavoriteView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login_page")

    def get(self, request):
        if "product_id" in request.GET:
            product_id = request.GET["product_id"]
            product = Product.objects.get(pk=product_id)
            user = request.user
            user.favorite_products.remove(product)
            return HttpResponse("Product removed to favorite")
        return HttpResponse("Product id not found error!")
