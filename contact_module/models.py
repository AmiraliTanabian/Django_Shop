from django.db import models


class ContactModel(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    subject = models.CharField(max_length=255, verbose_name="موضوع")
    msg = models.TextField(verbose_name="متن پیام")
    is_read = models.BooleanField(verbose_name="خوانده شده", default=False)

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام ها"

    def __str__(self):
        return self.subject
