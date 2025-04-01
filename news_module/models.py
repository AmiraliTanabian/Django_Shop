from django.db import models
from django.contrib.auth.models import AbstractUser
from django_jalali.db.models import jDateTimeField
from django.contrib.auth import get_user_model

class User(AbstractUser):
    about_user = models.TextField(null=True, blank=True, verbose_name="درباره کاربر")
    profile_image = models.ImageField(upload_to="Images/user_profile", verbose_name="آواتار کاربر",
                                      null=True, blank=True)


    def __str__(self):
        if self.first_name != '' and self.last_name != '':
            return self.get_full_name()

        if self.username is not None:
            return self.username
        return self.email

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربر ها"

User_model = get_user_model()

class ArticleTag(models.Model):
    tag_name = models.CharField(max_length=100, verbose_name="نام تگ")
    slug = models.SlugField(max_length=100, verbose_name="اسلاگ", null=True, unique=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "تگ مقاله"
        verbose_name_plural = "تگ های مقالات"

    def __str__(self):
        return self.tag_name

class ArticleCategories(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               verbose_name="دسته بندی والد(اختیاری)", null=True, blank=True,
                               related_name="category_child")
    title = models.CharField(max_length=25, verbose_name="نام دسته بندی")
    slug = models.SlugField(max_length=25, verbose_name="اسلاگ", null=True, unique=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "دسته بندی مقاله"
        verbose_name_plural = "دسته بندی های مقالات"

class Article(models.Model):
    title = models.CharField(max_length=300, verbose_name="عنوان")
    author = models.ForeignKey(User_model, on_delete=models.PROTECT, verbose_name="نویسندخ مقاله")
    categories = models.ManyToManyField(ArticleCategories, verbose_name="دسته بندی ها")
    image = models.ImageField(upload_to="Images/BLog", verbose_name="عکس اصلی")
    tags = models.ManyToManyField(ArticleTag, verbose_name="تگ ها", related_name="article_list_by_tag")
    short_info = models.CharField(max_length=255, verbose_name="توضیحات کوتاه")
    text = models.TextField(verbose_name="متن خبر")
    data = jDateTimeField(verbose_name="تاریخ و زمان", auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def __str__(self):
        return self.title

class ArticleComment(models.Model):
    user = models.ForeignKey(User_model, on_delete=models.CASCADE, verbose_name="کاربر")
    parent = models.ForeignKey("self", on_delete=models.CASCADE,
                               verbose_name="نظر والد (اختیاری)", blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="مقاله")
    text = models.TextField(verbose_name="متن نظر")
    created_at = jDateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False, verbose_name="فعال بودن نظر")

    class Meta:
        verbose_name = "نظر برای مقاله"
        verbose_name_plural = "نظرات برای مقاله ها"

    def __str__(self):
        return str(self.user)