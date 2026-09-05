# from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django_jalali.db.models import jDateTimeField


class ContactModel(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام")
    date = jDateTimeField(verbose_name="تاریخ", auto_now_add=True, blank=True, null=True)
    email = models.EmailField(verbose_name="ایمیل")
    subject = models.CharField(max_length=255, verbose_name="موضوع")
    msg = models.TextField(verbose_name="متن پیام")
    answer = models.TextField(verbose_name="متن پاسخ", null=True, blank=True)
    answer_date = jDateTimeField(verbose_name="تاریخ پاسخ", null=True, blank=True)
    answer_admin = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                        verbose_name="ادمین پاسخ دهنده ",
                                        null=True,
                                        blank=True)
    is_read = models.BooleanField(verbose_name="خوانده شده", default=False)

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام ها"

    def __str__(self):
        return self.subject
