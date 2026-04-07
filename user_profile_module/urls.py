from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProfileDashboardPage.as_view(), name="profile_page"),
    path("edit-profile", views.EditProfilePageView.as_view(), name="edit_profile_page"),
    path("edit-password", views.EditPasswordPageView.as_view(), name="edit_password_page"),
    path("favorite-list", views.ProfileFavoriteProductsView.as_view(), name="favorite_list_on_profile"),
    path("orders", views.ProfileOrders.as_view(), name="profile_order_page"),
    path("order/<int:pk>", views.orderPageView.as_view(), name="order_detail_page"),
    path("ticket/add/", views.AddTickerView.as_view(), name="add_ticket_page"),
    path("ticket/list/", views.TicketList.as_view(), name="ticket_list_page"),
    path("ticket/detial/<int:id>", views.TicketList.as_view(), name="ticket_detail_page"),
]
