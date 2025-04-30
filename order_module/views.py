# import json
#
# import requests
# from django.conf import settings
# from django.http import HttpRequest, HttpResponse, JsonResponse
# from django.shortcuts import render, redirect
# from django.urls import reverse_lazy
# from django.views import View
# from django.views.generic import ListView
# from django.contrib.auth.decorators import login_required
#
# from .models import orderModel, orderProductModel
#
#
# class AddProductToOrder(View):
#     def get(self, request: HttpRequest):
#         if request.user.is_authenticated:
#             order = orderModel.objects.filter(user=request.user, is_paid=False).first()
#             product_count = int(request.GET.get("count"))
#
#             if not order:
#                 order = orderModel.objects.create(user=request.user)
#
#             order_product = orderProductModel.objects.filter(order=order,
#                                                              product_id=request.GET["product_id"]).first()
#             if product_count < 1:
#                 return JsonResponse({
#                     "status": "invalid_count_value",
#                     "title": "تعداد نامعبر!",
#                     "text": "تعداد مورد نظر نباید 0 یا منفی باشد!",
#                     "icon": "warning",
#                 })
#
#             # check the product on order exists or no
#             if not order_product:
#                 new_order_product = orderProductModel(order=order, count=product_count,
#                                                       product_id=request.GET["product_id"])
#                 new_order_product.save()
#
#             else:
#                 order_product.count += product_count
#                 order_product.save()
#
#             return JsonResponse({
#                 "status": "success",
#                 "title": "موفق!",
#                 "text": "محصول به سبد خرید اضافه شد!",
#                 "icon": "success",
#             })
#
#         return JsonResponse({
#             "status": "not_auth",
#             "title": "وارد حساب نشدید!",
#             "text": "شما باید وارد حساب خود شوید",
#             "icon": "error",
#         })
#
#
# class OrderPage(ListView):
#     template_name = "order_module/order_page.html"
#     model = orderModel
#     context_object_name = "products"
#
#     def get_queryset(self):
#         query: orderModel = self.model.objects.filter(user=self.request.user, is_paid=False).first()
#         if query:
#             query = query.orderproductmodel_set.all()
#         else:
#             query = list()
#         return query
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         order = self.model.objects.filter(user=self.request.user, is_paid=False).first()
#
#         if order:
#             total_price = order.total_order_price()
#             context["total_price"] = total_price
#         return context
#
#
# class RemoveFromOrder(View):
#     def get(self, request: HttpRequest):
#         if request.user.is_authenticated:
#             product_id = request.GET.get("product_id")
#
#             if product_id is None:
#                 return JsonResponse({
#                     "status": "product id not found"
#                 })
#
#             order, is_created_new_order = orderModel.objects.get_or_create(user=request.user, is_paid=False)
#
#             order_product = orderProductModel.objects.get(order=order,
#                                                           product__id=int(product_id))
#             order_product.delete()
#
#             if order:
#                 query = order.orderproductmodel_set.all()
#             else:
#                 query = list()
#
#             total_price = order.total_order_price()
#             return render(request, "order_module/order_list_ajax.html", {
#                 "products": query,
#                 "total_price": total_price,
#             })
#
#         return HttpResponse("User authentication is failed!")
#
#
# class AddProductCountView(View):
#     def get(self, request: HttpRequest):
#         if request.user.is_authenticated:
#             product_id = request.GET["product_id"]
#             order: orderModel = orderModel.objects.filter(user=self.request.user, is_paid=False).first()
#             order_product = order.orderproductmodel_set.get(product__id=product_id)
#             order_product.count += 1
#             order_product.save()
#
#             # Get the current product after remove
#             query = order.orderproductmodel_set.all()
#
#             total_price = order.total_order_price()
#             return render(request, "order_module/order_list_ajax.html", {
#                 "products": query,
#                 "total_price": total_price,
#             })
#
#         return HttpResponse("User authentication is failed!")
#
#
# class RemoveProductCountView(View):
#     def get(self, request: HttpRequest):
#         if request.user.is_authenticated:
#             product_id = request.GET["product_id"]
#             order: orderModel = orderModel.objects.filter(user=self.request.user, is_paid=False).first()
#             order_product = order.orderproductmodel_set.get(product__id=product_id)
#             order_product.count -= 1
#             order_product.save()
#
#             # Get the current product after remove
#             query = order.orderproductmodel_set.all()
#
#             total_price = order.total_order_price()
#             return render(request, "order_module/order_list_ajax.html", {
#                 "products": query,
#                 "total_price": total_price,
#             })
#
#         return HttpResponse("User authentication is failed!")
#
#
# #  Zarinpal payment config
#
# # ? sandbox merchant
# if settings.SANDBOX:
#     sandbox = 'sandbox'
#
# else:
#     sandbox = 'www'
#
# ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
#
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# phone = 'YOUR_PHONE_NUMBER'  # Optional
# # Important: need to edit for realy server.
# CallbackURL = 'http://127.0.0.1:8080/verify/'
#
#
# @login_required
# def payment_request(request: HttpRequest):
#     current_order = orderModel.objects.filter(is_paid=False, user=request.user).first()
#     total_price = current_order.total_order_price()
#
#     # Check the basket not empty
#     if total_price == 0:
#         return redirect(reverse_lazy("order_page"))
#
#     data = {
#         "MerchantID": settings.MERCHANT,
#         # Convert to Rial
#         "Amount": total_price * 10,
#         "Description": description,
#         "Phone": phone,
#         "CallbackURL": CallbackURL,
#     }
#     data = json.dumps(data)
#     # set content length by data
#     headers = {'content-type': 'application/json', 'content-length': str(len(data))}
#     try:
#         response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
#
#         if response.status_code == 200:
#             response = response.json()
#             if response['Status'] == 100:
#                 return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
#                         'authority': response['Authority']}
#             else:
#                 return {'status': False, 'code': str(response['Status'])}
#         return response
#
#     except requests.exceptions.Timeout:
#         return {'status': False, 'code': 'timeout'}
#     except requests.exceptions.ConnectionError:
#         return {'status': False, 'code': 'connection error'}
#
#
# @login_required
# def payment_verify(request: HttpRequest, authority):
#     current_order = orderModel.objects.filter(is_paid=False, user=request.user).first()
#     total_price = current_order.total_order_price()
#
#     data = {
#         "MerchantID": settings.MERCHANT,
#         # Convert to Rial
#         "Amount": total_price * 10,
#         "Authority": authority,
#     }
#     data = json.dumps(data)
#     # set content length by data
#     headers = {'content-type': 'application/json', 'content-length': str(len(data))}
#     response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
#
#     if response.status_code == 200:
#         response = response.json()
#         if response['Status'] == 100:
#             # close the order
#             current_order.is_paid = True
#             current_order.save()
#
#             ref_id = response['RefID']
#             return render(request, "order_module/payment_result.html", {
#                 "success": "پرداخت شما با کد پیگیری {} با موفقیت انجام شد".format(ref_id)
#             })
#         else:
#             code = str(response['Status'])
#             return render(request, "order_module/payment_result.html", {
#                 "error": "پرداخت با خطا مواجه شد \n کد خطا : {} ".format(code)
#             })
#     return response
