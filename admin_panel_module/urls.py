from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_page, name="admin_index_page"),
    path('articles', views.ArticlePageView.as_view(), name="admin_articles_page"),
    path("article/<int:pk>", views.EditArticleView.as_view(), name="admin_article_detail_page"),
    path('contact-us/', views.ContactUSAdminView.as_view(), name="contact_us_admin_page"),
    path("contact-us/<int:pk>", views.MessageDetailView.as_view(), name="message-detail-page"),
    path('contact-us/remove-msg/', views.RemoveMessageAdminView.as_view(), name="remove_msg_from_admin_ajax"),
    path("contact-us/send-ans/", views.SendMsgAnswer.as_view(), name="send_ans_from_admin_ajax"),
    path("settings/slider/", views.sliderList.as_view(), name="sliders"),
    path("settings/slider/<int:pk>", views.sliderDetail.as_view(), name="slider_detail"),
    path("settings/add-slider/", views.addSliderView.as_view(), name="add_slider_page"),
    path("settings/slider/remove-slider/", views.RemoveSliderView.as_view(), name="remove_slider_page"),
    path("settings/slider/set-slider-enable/", views.SetSliderEnableView, name="set_slider_enable_ajax"),
    path("settings/slider/set-slider-disable/", views.SetSliderDisableView, name="set_slider_disable_ajax"),
    path("settings/site-setting/", views.SiteSettingEditView.as_view(), name="site_setting_page"),
]
