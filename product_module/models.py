from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


class Brand(models.Model):
    title = models.CharField(max_length=50, verbose_name="عنوان برند")
    slug = models.SlugField(verbose_name="اسلاگ", allow_unicode=True, db_index=True, unique=True)
    is_active = models.BooleanField(verbose_name="فعال")

    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برند ها"

    def __str__(self):
        return self.title

    def get_product_count_with_brand(self):
        # TODO; Develop with annotate
        count = Product.objects.filter(brand=self).count()
        return count


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


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="عنوان محصول ")
    price = models.BigIntegerField(verbose_name="مبلغ")
    banner = models.ImageField(upload_to="Images/product", verbose_name="تصویر محصول")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name="برند")
    categories = models.ManyToManyField(ProductCategory, verbose_name="دسته بندی ها")
    count = models.IntegerField(verbose_name="تعداد موجودی", validators=[
        MinValueValidator(0, "حداقل موجودی کالا ۰ میباشد!")
    ], null=True)
    is_active = models.BooleanField(verbose_name="فعال", default=True)
    is_available = models.BooleanField(verbose_name="موجودی", default=True)
    is_new = models.BooleanField(verbose_name="کالا جدید است", default=True)

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
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, verbose_name="والد ( اختیاری )")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="کاربر")
    text = models.TextField(verbose_name="متن نظر")

    class Meta:
        verbose_name = "نظر محصول"
        verbose_name_plural = "نظرات محصول"

    def __str__(self):
        return f'{str(self.user)} | {str(self.product)}'
