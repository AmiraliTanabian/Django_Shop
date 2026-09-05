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
    path("contact-us/", views.ContactUsListView.as_view(), name="admin_contact_us_list"),
    path("contact-us/<id>", views.ContactUsDetailView.as_view(), name="admin_contact_detail_page"),
    path("contact-us/send-answer/", views.send_msg_answer_ajax, name="admin_contact_send_email_ajax"),
    path("blog/list/", views.BlogListView.as_view(), name="admin_blog_list_page"),
    path("blog/<id>", views.BlogEditPage.as_view(), name="admin_blog_edit_page"),
]
