from django.contrib import admin

from .models import ProductCategory, Product, Brand, ProductGallery, ProductComment


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active"]
    list_filter = ["is_active"]
    list_editable = ["is_active"]
    prepopulated_fields = {
        "slug": ("title",)
    }


class BrandAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active"]
    list_filter = ["is_active"]
    list_editable = ["is_active"]
    prepopulated_fields = {
        "slug": ("title",)
    }


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "banner"]
    list_filter = ["is_active"]
    list_editable = ["is_active"]


class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ["product", "banner", "is_active"]
    list_editable = ["is_active"]


admin.site.register(Brand, BrandAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGallery, ProductGalleryAdmin)
admin.site.register(ProductComment)
