from django.http import HttpRequest
from django.http import JsonResponse
from django.views import View

from .models import newsLetterModel


class AddMailToNewsLetter(View):
    def post(self, request: HttpRequest):
        email = request.POST.get("email")
        email_on_db = newsLetterModel.objects.filter(is_active=True, email__iexact=email).first()

        if not email_on_db:
            new_email = newsLetterModel(email=email)
            new_email.save()

            return JsonResponse({
                "title": "افزوده شدن ایمیل",
                "text": "ایمیل شما با موفقیت افزوده شد",
                "icon": 'success'
            })

        return JsonResponse({
            "title": "تکراری بودن ایمیل",
            "text": "این ایمیل قبلا در خبرنامه وجود دارد :)",
            "icon": 'error'
        })
