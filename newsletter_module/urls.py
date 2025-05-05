from django.urls import path

from .views import AddMailToNewsLetter

urlpatterns = [
    path("add/", AddMailToNewsLetter.as_view(), name="add_mail_to_news_letter"),
]
