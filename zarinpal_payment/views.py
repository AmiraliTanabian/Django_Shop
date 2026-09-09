import json
import logging
from datetime import datetime

import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from order_module.models import orderModel, orderStatus

logger = logging.getLogger(__name__)

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

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/v4/payment/request.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/v4/payment/verify.json"

REQUEST_TIMEOUT = 15  # ثانیه - قابل تنظیم


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
                ref_id = response['data'].get("ref_id")

                current_order.is_paid = True
                current_order.paid_date = datetime.now()
                current_order.set_finally_price()
                current_order.set_product_order_count()
                current_order.status = orderStatus.pendingـreview
                current_order.payment_id = ref_id
                current_order.save()
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


@login_required
def request_payment(request: HttpRequest):
    current_order = orderModel.objects.get(is_paid=False, user=request.user)
    total_price = current_order.total_order_price() * 10

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

    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.Timeout:
        logger.error("Zarinpal request timed out")
        return HttpResponse("درگاه پرداخت پاسخ نداد، لطفاً دوباره تلاش کنید.")
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Zarinpal connection error: {e}")
        return HttpResponse("اتصال به درگاه پرداخت برقرار نشد، لطفاً دوباره تلاش کنید.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Zarinpal request failed: {e}")
        return HttpResponse("مشکلی پیش آمد.")

    if response.status_code == 200:
        response_data = response.json()
        if response_data["data"]['code'] == 100:
            url = f"{ZP_API_STARTPAY}{response_data['data']['authority']}"
            return redirect(url)
        else:
            logger.error(f"Zarinpal returned error: {response_data.get('errors')}")
            return HttpResponse(str(response_data['errors']))
    else:
        logger.error(f"Zarinpal non-200 response: {response.status_code} - {response.text}")
        return HttpResponse("مشکلی پیش آمد.")
