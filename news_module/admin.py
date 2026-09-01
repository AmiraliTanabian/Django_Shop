from django.contrib import admin

from .models import Article, ArticleTag, ArticleCategories, ArticleComment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "short_info", "is_active"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]

    readonly_fields = ("author",)

    def save_model(self, request, obj, form, change):
        # the article created 
        print("i am here2")

        if not change:
            print("i am here")
            obj.author = request.user

        super().save_model(request, obj, form, change)
    
 

class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ["tag_name", "is_active"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]
    prepopulated_fields = {"slug": ("tag_name",)}


class ArticleCategoriesAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active"]
    list_filter = ["is_active"]
    list_editable = ["is_active"]

    prepopulated_fields = {"slug": ("title",)}


class ArticleCommentsAdmin(admin.ModelAdmin):
    list_display = ["user", "parent", "is_active"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleTag, ArticleTagAdmin)
admin.site.register(ArticleCategories, ArticleCategoriesAdmin)
admin.site.register(ArticleComment, ArticleCommentsAdmin)
