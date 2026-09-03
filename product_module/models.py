from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_jalali.db.models import jDateTimeField


class Brand(models.Model):
    title = models.CharField(max_length=50, verbose_name="عنوان برند")
    slug = models.SlugField(verbose_name="اسلاگ", allow_unicode=True, db_index=True, unique=True)
    is_active = models.BooleanField(verbose_name="فعال")

    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برند ها"

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    parent = models.ForeignKey("self", on_delete=models.CASCADE, verbose_name="والد (اختیاری)", null=True, blank=True,
                               related_name="childs")
    title = models.CharField(max_length=50, verbose_name="عنوان دسته بندی")
    slug = models.SlugField(verbose_name="اسلاگ", allow_unicode=True, db_index=True, unique=True)
    is_active = models.BooleanField(verbose_name="فعال")

    class Meta:
        verbose_name = "دسته بندی محصول"
        verbose_name_plural = "دسته بندی های محصول"

    def __str__(self):
        return self.title


class ProductTag(models.Model):
    tag_name = models.CharField(max_length=100, verbose_name="نام تگ")
    slug = models.SlugField(max_length=100, verbose_name="اسلاگ", null=True, unique=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "تگ محصول"
        verbose_name_plural = "تگ های محصولات"

    def __str__(self):
        return self.tag_name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="عنوان محصول ")
    price = models.BigIntegerField(verbose_name="مبلغ", validators=[
        MinValueValidator(0, "حداقل مبلغ محصول ۰ میباشد!")
    ])
    banner = models.ImageField(upload_to="Images/product", verbose_name="تصویر محصول")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name="برند", related_name="products")
    categories = models.ManyToManyField(ProductCategory, verbose_name="دسته بندی ها")
    tags = models.ManyToManyField(ProductTag, verbose_name="تگ های محصول", related_name="product_tags")
    count = models.IntegerField(verbose_name="تعداد موجودی", validators=[
        MinValueValidator(0, "حداقل موجودی کالا ۰ میباشد!")
    ], null=True)
    info = models.TextField(verbose_name="توضیحات", null=True)
    is_active = models.BooleanField(verbose_name="فعال", default=True)
    is_available = models.BooleanField(verbose_name="موجودی", default=True)
    is_new = models.BooleanField(verbose_name="کالا جدید است", default=True)
    order_count = models.PositiveIntegerField(verbose_name="تعداد سفارش از این محصول", editable=False, default=0)

    class Meta:
        verbose_name = "کالا"
        verbose_name_plural = "کالا ها"

    def __str__(self):
        return self.name


class ProductView(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name="کاربر", null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    ip = models.CharField(max_length=20, verbose_name="آی پی")


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    banner = models.ImageField(upload_to="products_gallery", verbose_name="تصویر")
    is_active = models.BooleanField(default=True, verbose_name="فعال / غیرفعال")

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = "گالری محصول"
        verbose_name_plural = "گالری محصولات"


class ProductComment(models.Model):
    class StatusChoices(models.TextChoices):
        approved = ("approved", "تایید شده")
        pending = ("pending", "در انتظار تایید")
        rejected = ("rejected", "رد شده")

    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, verbose_name="والد ( اختیاری )")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="کاربر")
    text = models.TextField(verbose_name="متن نظر")
    date = jDateTimeField(verbose_name="تاریخ", auto_now_add=True)
    score = models.IntegerField(verbose_name="امتیاز کاربر",
                                validators=[
                                    MaxValueValidator(5, "امتیاز نمیتواند بیشتر از ۵ باشد"),
                                    MinValueValidator(0, "امتیاز نمیتواند کمتر از ۰ باشد"),
                                ], null=True, )
    status = models.CharField(max_length=255, verbose_name="وضعیت کامنت", choices=StatusChoices,
                              default="pending")
    is_active = models.BooleanField(verbose_name="فعال بودن / نبودن", default=True)
    has_unread_reply = models.BooleanField(verbose_name="داشتن پاسخ خوانده نشده", default=False)

    class Meta:
        verbose_name = "نظر محصول"
        verbose_name_plural = "نظرات محصول"

    def __str__(self):
        return f'{str(self.user)} | {str(self.product)}'

    def comment_score_range(self):
        return range(self.score)
