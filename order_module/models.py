from django.contrib.auth import get_user_model
from django.db import models
from django_jalali.db.models import jDateTimeField

from product_module.models import Product


class orderModel(models.Model):
    user = models.ForeignKey(get_user_model(), verbose_name="کاربر", on_delete=models.CASCADE)
    paid_date = jDateTimeField(verbose_name="تاریخ پرداخت", null=True)
    is_paid = models.BooleanField(verbose_name="پرداخت شده / نشده", default=False)

    def __str__(self):
        return '{} -- {}'.format(self.id, str(self.user))

    def total_order_price(self):
        total_amount = 0
        if self.is_paid:
            for product in self.orderproductmodel_set.all():
                total_amount += product.finally_price * product.count
        else:
            for product in self.orderproductmodel_set.all():
                total_amount += product.product.price * product.count
        return (total_amount)

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبد های خرید"


class orderProductModel(models.Model):
    order = models.ForeignKey(orderModel, on_delete=models.CASCADE, verbose_name="سبد خرید")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    count = models.IntegerField(verbose_name="تعداد", default=1)
    finally_price = models.BigIntegerField(verbose_name="قیمت نهایی محصول", null=True)

    def total_price(self):
        return self.product.price * self.count

    def __str__(self):
        return '{} - {}'.format(str(self.order), str(self.product))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "کالای سبد خرید"
        verbose_name_plural = "کالاهای سبد خرید"
