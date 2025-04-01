from django.db import models
from django.contrib.auth.models import AbstractUser

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

class TempUser(models.Model):
    username = models.CharField(max_length=150, verbose_name="نام کاربری")
    password = models.CharField(max_length=150, verbose_name="رمز عبور")
    email = models.EmailField(verbose_name="ایمیل")
    random_string = models.CharField(max_length=72, verbose_name="عبارت فعال سازی")
    data = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "کاربر موقت"
        verbose_name_plural = "کاربران موقت"
