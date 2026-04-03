from django.urls import path

from . import views

urlpatterns = [
    path('request/', views.request_payment, name='request_payment'),
    path('verify/', views.verify_payment, name='verify_payment')
]
