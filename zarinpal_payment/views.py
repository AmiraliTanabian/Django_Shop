import json

import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.timezone import now

from order_module.models import orderModel
from . import zarinpal_config

if zarinpal_config.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'payment'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/v4/payment/request.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/v4/payment/verify.json"

description = "نهایی کردن خرید شما از سایت ما"  # it's only an example

CallbackURL = 'http://localhost:8000/payment/verify/'  # you should customize it


@login_required
def request_payment(request: HttpRequest):
    current_order = orderModel.objects.get(is_paid=False, user=request.user)
    total_price = current_order.total_order_price() * 10  # *10 : Convert from Toman to Rial

    if total_price == 0:
        return redirect(reverse("home_page"))

    data = {
        "merchant_id": zarinpal_config.MERCHANT,
        "amount": total_price,
        "description": description,
        "callback_url": CallbackURL,
    }
    data = json.dumps(data)

    headers = {'content-type': 'application/json', 'content-length': str(len(data))}

    response = requests.post(ZP_API_REQUEST, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()

        if response["data"]['code'] == 100:
            url = f"{ZP_API_STARTPAY}{response["data"]['authority']}"
            return redirect(url)

        else:
            return HttpResponse(str(response['errors']))

    else:
        return HttpResponse("مشکلی پیش آمد.")


@login_required
def verify_payment(request: HttpRequest):
    current_order = orderModel.objects.get(is_paid=False, user=request.user)
    total_price = current_order.total_order_price() * 10  # *10 : Convert from Toman to Rial

    status = request.GET.get('Status')
    authority = request.GET['Authority']

    if status == "OK":
        data = {
            "merchant_id": zarinpal_config.MERCHANT,
            "amount": total_price,
            "authority": authority
        }
        data = json.dumps(data)

        headers = {'content-type': 'application/json', 'Accept': 'application/json'}

        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['data']['code'] == 100:
                current_order.is_paid = True
                current_order.paid_date = now()
                current_order.set_finally_price()
                current_order.save()
                ref_id = response['data'].get("ref_id")
                return render(request, 'zarinpal_payment/payment_result.html', {
                    'success': f"پرداخت شما با موفقیت انجام گردید \n شناسه پرداخت :{ref_id}"
                })


            elif response['data']['code'] == 101:
                return render(request, 'zarinpal_payment/payment_result.html', {
                    'info': "این پرداخت قبلا انجام شده است."
                })


            else:
                return render(request, 'zarinpal_payment/payment_result.html', {
                    'error': 'پرداخت با خطا مواجه شد / کاربر از پرداخت ممانعت کرد \n در صورت کسر مبلغ تا ۷۲ ساعت به حساب شما باز میگردد'
                })

        else:
            return render(request, 'zarinpal_payment/payment_result.html', {
                'error': 'پرداخت با خطا مواجه شد / کاربر از پرداخت ممانعت کرد \n در صورت کسر مبلغ تا ۷۲ ساعت به حساب شما باز میگردد'
            })

    else:
        return render(request, 'zarinpal_payment/payment_result.html', {
            'error': 'پرداخت با خطا مواجه شد / کاربر از پرداخت ممانعت کرد \n در صورت کسر مبلغ تا ۷۲ ساعت به حساب شما باز میگردد'
        })
