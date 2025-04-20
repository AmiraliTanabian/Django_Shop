from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .models import orderModel, orderProductModel


class AddProductToOrder(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            order = orderModel.objects.filter(user=request.user, is_paid=False).first()
            product_count = request.POST.get(["count"])

            if not order:
                order = orderModel.objects.create(user=request.user)

            order_product = orderProductModel.objects.filter(order=order,
                                                             product_id=request.GET["product_id"]).first()
            if order_product is None:
                return HttpResponse("Product not found!")

            if int(product_count) > 1:
                return JsonResponse({
                    "status": "invalid_count_value"
                })

            # check the product on order exists or no
            if not order_product:
                new_order_product = orderProductModel(order=order, count=int(product_count),
                                                      product_id=request.GET["product_id"])
                new_order_product.save()

            else:
                order_product.count += int(self.request.GET["count"])
                order_product.save()

            return HttpResponse("Order added!")

        return HttpResponse("User dont login")


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


class RemoveFromOrder(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            product_id = request.GET["product_id"]
            order = orderModel.objects.get(user=request.user)
            order_product = orderProductModel.objects.get(order=order,
                                                          product__id=product_id)
            order_product.delete()

            # Get the current product after remove
            query: orderModel = orderModel.objects.filter(user=self.request.user, is_paid=False).first()
            if query:
                query = query.orderproductmodel_set.all()
            else:
                query = list()

            return render(request, "order_module/order_list_ajax.html", {
                "products": query,
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

            return render(request, "order_module/order_list_ajax.html", {
                "products": query,
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

            return render(request, "order_module/order_list_ajax.html", {
                "products": query,
            })
        return HttpResponse("User authentication is failed!")
