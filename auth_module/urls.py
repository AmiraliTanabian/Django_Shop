from django.urls import path
from .views import loginView, registerView

urlpatterns = [
    path("login", loginView.as_view(), name="login_page"),
    path("register", registerView.as_view(), name="register_page"),
]