from django.contrib import admin
from .models import ArticleCategoryModel, ArticleModel
# Register your models here.
admin.site.register(ArticleModel)
admin.site.register(ArticleCategoryModel)