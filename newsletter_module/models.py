from django.db import models


class newsLetterModel(models.Model):
    email = models.EmailField(verbose_name="ایمیل")
    is_active = models.BooleanField(verbose_name="فعال / غیرفعال", default=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "ایمیل خبرنامه"
        verbose_name_plural = "ایمیل های خبرنامه"
