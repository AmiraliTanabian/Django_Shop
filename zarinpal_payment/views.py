import json

import requests
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect

from . import zarinpal_config

if zarinpal_config.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'payment'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/v4/payment/request.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/v4/payment/verify.json"

description = "نهایی کردن خرید شما از سایت ما"  # it's only an example

price = 100000  # it's only an example
CallbackURL = 'http://localhost:8000/payment/verify/'  # you should customize it


def request_payment(request: HttpRequest):
    data = {
        "merchant_id": zarinpal_config.MERCHANT,
        "amount": price,
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


def verify_payment(request: HttpRequest):
    status = request.GET.get('Status')
    authority = request.GET['Authority']

    if status == "OK":
        data = {
            "merchant_id": zarinpal_config.MERCHANT,
            "amount": price,
            "authority": authority
        }
        data = json.dumps(data)

        headers = {'content-type': 'application/json', 'Accept': 'application/json'}

        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['data']['code'] == 100:
                # put your logic here
                return HttpResponse("خرید شما با موفقیت انجام شد.")

            elif response['data']['code'] == 101:
                return HttpResponse("این پرداخت قبلا انجام شده است.")

            else:
                return HttpResponse("پرداخت شما ناموفق بود.")

        else:
            return HttpResponse("پرداخت شما ناموفق بود.")

    else:
        return HttpResponse("پرداخت شما ناموفق بود.")
