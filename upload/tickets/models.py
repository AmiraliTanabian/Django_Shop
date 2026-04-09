from django.db import models
from django_jalali.db.models import jDateTimeField

class ArticleCategoryModel(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان دسته بندی مثاله")
    slug = models.SlugField(verbose_name="اسلاگ")

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = "دسته بندی مقاله"
        verbose_name_plural = "دسته بندی های مقالات"

class ArticleModel(models.Model):
    title = models.CharField(verbose_name="عنوان مقاله", max_length=200)
    date = jDateTimeField(verbose_name="تاریخ", auto_now=True)
    category = models.ForeignKey(ArticleCategoryModel, verbose_name="دسته بندی", on_delete=models.PROTECT)
    text = models.TextField(verbose_name = "متن مقاله")
    banner = models.ImageField(upload_to="blog_banner", verbose_name="بنر مقاله")
    is_active = models.BooleanField(verbose_name="فعال - غیرفعال", default=True)

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = "پست"
        verbose_name_plural = "پست ها"