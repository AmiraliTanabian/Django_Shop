from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProfileDashboardPage.as_view(), name="profile_page")
]