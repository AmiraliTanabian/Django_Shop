from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .models import orderModel, orderProductModel


class AddProductToOrder(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            order = orderModel.objects.filter(user=request.user, is_paid=False).first()

            try:
                product_count = int(request.GET.get("count"))
            except TypeError:
                product_count = 1

            if not order:
                order = orderModel.objects.create(user=request.user)

            order_product = orderProductModel.objects.filter(order=order,
                                                             product_id=request.GET["product_id"]).first()
            if product_count < 1:
                return JsonResponse({
                    "status": "invalid_count_value",
                    "title": "تعداد نامعبر!",
                    "text": "تعداد مورد نظر نباید 0 یا منفی باشد!",
                    "icon": "warning",
                })

            # check the product on order exists or no
            if not order_product:
                new_order_product = orderProductModel(order=order, count=product_count,
                                                      product_id=request.GET["product_id"])
                new_order_product.save()

            else:
                order_product.count += product_count
                order_product.save()

            return JsonResponse({
                "status": "success",
                "title": "موفق!",
                "text": "محصول به سبد خرید اضافه شد!",
                "icon": "success",
            })

        return JsonResponse({
            "status": "not_auth",
            "title": "وارد حساب نشدید!",
            "text": "شما باید وارد حساب خود شوید",
            "icon": "error",
        })


class OrderPage(ListView):
    template_name = "order_module/order_page.html"
    model = orderModel
    context_object_name = "products"

    def get_queryset(self):
        query: orderModel = self.model.objects.filter(user=self.request.user, is_paid=False).first()
        if query:
            query = query.orderproductmodel_set.all()
        else:
            query = list()
        return query

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        order = self.model.objects.filter(user=self.request.user, is_paid=False).first()

        if order:
            total_price = order.total_order_price()
            context["total_price"] = total_price
        return context


class RemoveFromOrder(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            product_id = request.GET.get("product_id")

            if product_id is None:
                return JsonResponse({
                    "status": "product id not found"
                })

            order, is_created_new_order = orderModel.objects.get_or_create(user=request.user, is_paid=False)

            order_product = orderProductModel.objects.get(order=order,
                                                          product__id=int(product_id))
            order_product.delete()

            if order:
                query = order.orderproductmodel_set.all()
            else:
                query = list()

            total_price = order.total_order_price()
            return render(request, "order_module/order_list_ajax.html", {
                "products": query,
                "total_price": total_price,
            })

        return HttpResponse("User authentication is failed!")


class AddProductCountView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            product_id = request.GET["product_id"]
            order: orderModel = orderModel.objects.filter(user=self.request.user, is_paid=False).first()
            order_product = order.orderproductmodel_set.get(product__id=product_id)
            order_product.count += 1
            order_product.save()

            # Get the current product after remove
            query = order.orderproductmodel_set.all()

            total_price = order.total_order_price()
            return render(request, "order_module/order_list_ajax.html", {
                "products": query,
                "total_price": total_price,
            })

        return HttpResponse("User authentication is failed!")


class RemoveProductCountView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            product_id = request.GET["product_id"]
            order: orderModel = orderModel.objects.filter(user=self.request.user, is_paid=False).first()
            order_product = order.orderproductmodel_set.get(product__id=product_id)
            order_product.count -= 1
            order_product.save()

            # Get the current product after remove
            query = order.orderproductmodel_set.all()

            total_price = order.total_order_price()
            return render(request, "order_module/order_list_ajax.html", {
                "products": query,
                "total_price": total_price,
            })

        return HttpResponse("User authentication is failed!")
