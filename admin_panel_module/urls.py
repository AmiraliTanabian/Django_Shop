from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name="admin_index_page"),
]
