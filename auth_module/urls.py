from django.urls import path
from .views import loginView, registerView, logoutView

urlpatterns = [
    path("login", loginView.as_view(), name="login_page"),
    path("register", registerView.as_view(), name="register_page"),
    path("logout", logoutView.as_view() , name="logout_page")
]