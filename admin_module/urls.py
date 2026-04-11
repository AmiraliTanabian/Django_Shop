from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="admin_home_page"),
    path("settings/", views.setting_page, name="admin_setting_page"),
]
