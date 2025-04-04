from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

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