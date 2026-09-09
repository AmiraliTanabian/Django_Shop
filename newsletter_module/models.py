from django.db import models
from django_jalali.db.models import jDateTimeField


class newsLetterModel(models.Model):
    email = models.EmailField(verbose_name="ایمیل")
    created_date = jDateTimeField(verbose_name="تاریخ ثبت خبرنامه", null=True, blank=True, auto_now_add=True)
    is_active = models.BooleanField(verbose_name="فعال / غیرفعال", default=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "ایمیل خبرنامه"
        verbose_name_plural = "ایمیل های خبرنامه"
