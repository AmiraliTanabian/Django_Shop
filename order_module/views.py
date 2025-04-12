from django.http import HttpRequest, HttpResponse
from django.views import View

from .models import orderModel, orderProductModel


class AddProductToOrder(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            order = orderModel.objects.filter(is_paid=False).first()

            if not order:
                order = orderModel.objects.create(user=request.user)

            order_product = orderProductModel.objects.filter(order=order,
                                                             product_id=request.GET["product_id"]).first()

            # check the product on order exists or no
            if not order_product:
                new_order_product = orderProductModel(order=order, count=int(request.GET["count"]),
                                                      product_id=request.GET["product_id"])
                new_order_product.save()

            else:
                order_product.count += int(self.request.GET["count"])
                order_product.save()

            return HttpResponse("Order added!")

        return HttpResponse("User dont login")
