from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProfileDashboardPage.as_view(), name="profile_page"),
    path("edit-profile", views.EditProfilePageView.as_view(), name="edit_profile_page"),
]