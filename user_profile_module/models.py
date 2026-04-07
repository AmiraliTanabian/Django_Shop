from django.contrib.auth import get_user_model
from django.db import models


class PriorityChoices(models.TextChoices):
    low = "low", "کم"
    medium = "medium", "متوسط"
    high = "high", "اهمیت بالا"


class UnitsChoices(models.TextChoices):
    TechnicalUnit = "TechnicalUnit", "واحد فنی"
    FinancialUnit = "FinancialUnit", "واحد مالی"
    OrderTracking = "OrderTracking", "پیگیری سفارش"


class ticket_model(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان تیکت")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="کاربر")
    Priority = models.CharField(max_length=255, verbose_name="اولویت", choices=PriorityChoices)
    Unit = models.CharField(max_length=255, verbose_name="واحد مربوطه", choices=UnitsChoices)
    text = models.CharField(max_length=255, verbose_name="متن تیکت")
    created_date = models.DateTimeField(verbose_name="تاریخ ساخت تیکت", auto_now_add=True)
    updated_date = models.DateTimeField(verbose_name="تاریخ بروزرسانی تیکت", auto_now=True)
    is_closed = models.BooleanField(verbose_name="بسته شدن تیکت")
    is_active = models.BooleanField(verbose_name="فعال / غیرفعال", default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = " تیکت"
        verbose_name_plural = "تیکت ها"


class ticket_attachment(models.Model):
    files = models.FileField(verbose_name="پیوست", upload_to="tickets")
    ticket = models.ForeignKey(ticket_model, on_delete=models.CASCADE, verbose_name="تیکت ها")

    class Meta:
        verbose_name = "پیوست تیکت"
        verbose_name_plural = " پیوست های تیکت ها"
