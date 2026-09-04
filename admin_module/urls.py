from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="admin_home_page"),
    path("settings/", views.main_setting_page, name="admin_setting_page"),
    path("settings/setting", views.MainSetting.as_view(), name="admin_setting_main_page"),
    path("settings/ads", views.SettingsAdsView.as_view(), name="admin_ads_setting_page"),
    path("settings/ads/<id>", views.AdsEditView.as_view(), name="ads_edit_page"),
    path("settings/sliders", views.SliderListPage.as_view(), name="admin_sliders_list_page"),
    path("settings/sliders/<id>", views.SliderDetailView.as_view(), name="admin_slider_edit_page"),
    path("settings/contact-us/", views.ContactUsListView.as_view(), name="admin_contact_us_list"),
]
