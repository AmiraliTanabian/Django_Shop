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

