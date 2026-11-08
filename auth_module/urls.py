from django.contrib.auth import views as auth_views
from django.urls import path

from .views import loginView, registerView, logoutView, verifyAccount, login_limited_view

urlpatterns = [
    path("login", loginView.as_view(), name="login_page"),
    path("register", registerView.as_view(), name="register_page"),
    path("logout", logoutView.as_view(), name="logout_page"),
    path("verify/<str:random_string>", verifyAccount.as_view(), name="verify_account"),
    path("login_limited", login_limited_view, name="login_limited_url"),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='auth_module/password_reset_form.html'
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='auth_module/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='auth_module/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
