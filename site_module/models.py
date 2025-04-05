from django.db import models

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, verbose_name="نام سایت")
    site_url = models.URLField(verbose_name="دامنه سایت")
    address = models.CharField(max_length=255, verbose_name="آدرس مجموعه")
    email = models.EmailField(max_length=50, verbose_name='ایمیل')
    phone = models.CharField(max_length=50, verbose_name="شماره تلفن")
    fax = models.CharField(max_length=255, verbose_name="فکس")
    copy_right = models.CharField(max_length=255, verbose_name="متن کپی رایت")
    about_us = models.TextField(verbose_name="متن درباره ما")
    site_logo = models.ImageField(upload_to="Images/site_settings/", verbose_name="لوگو سایت")
    is_active = models.BooleanField(verbose_name="فعال / غیرفعال")

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"

    def __str__(self):
        return self.site_name

class Slider(models.Model):
    title = models.CharField(max_length=50, verbose_name="عنوان اسلایدر")
    banner = models.ImageField(upload_to="Images/slider", verbose_name="عکس اسلایدر")
    text = models.CharField(max_length=255, verbose_name="متن اسلایدر")
    url = models.URLField(verbose_name="آدرس اسلایدر")
    btn_text = models.CharField(max_length=25, verbose_name="متن دکمه اسلایدر")
    is_active = models.BooleanField(verbose_name="فعال بودن اسلایدر", default=True)

    class Meta:
        verbose_name = "اسلایدر"
        verbose_name_plural = "اسلایدر ها"

    def __str__(self):
        return self.title
#
# [
#                                     ("product", "صفحه محصولات"),
#                                     ("contact", "صفحه تماس با ما"),
#                                     ("blog", "وبلاگ"),
#                                     ("about", "صفحه درباره ما"),
#                                     ("product_detail", "جزئیات محصول"),
#                                 ]

class SiteBanners(models.Model):
    class PositionChoices(models.TextChoices):
        product = "product", "صفحه محصولات"
        contact = "contact", "صفحه تماس با ما"
        blog = "blog", "وبلاگ"
        post_detail = "post_detail", "صفحه جزییات مقاله "
        product_detail = 'product_detail', "صفحه جزئیات محصول"
        posts = "posts", "صفحه مقالات"


    title = models.CharField(max_length=200, verbose_name="عنوان بنر")
    image = models.ImageField(upload_to="Images/Banner", verbose_name="تصویر")
    position = models.CharField(max_length=200, verbose_name="محل قرار گیری در سایت",
                                choices=PositionChoices)
    url = models.URLField(verbose_name="آدرس مقصد", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name="تبلیغ سایت"
        verbose_name_plural = "تبلیعات سایت"

    def __str__(self):
        return self.title