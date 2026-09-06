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
    path("blog/add/", views.BlogAddPage.as_view(), name="admin_add_blog_post"),
    path("blog/categories/", views.ArticleCategoriesList.as_view(), name="admin_blog_categories"),
    path("blog/add-cat/", views.AddArticleCategory.as_view(), name="admin_add_blog_category"),
    path("blog/tags/", views.AdminBlogTagsList.as_view(), name="admin_blog_tags"),

    path("blog/<id>/", views.BlogEditPage.as_view(), name="admin_blog_edit_page"),
    path("blog/remove-cat/<id>", views.remove_category_ajax, name="admin_blog_remove_category"),
    path("blog/remove-tag/<id>", views.remove_tag_ajax, name="admin_blog_remove_tag"),
    path("blog/set-active-cat/<id>/", views.set_blog_cat_active, name="admin_category_blog_set_active"),
    path("blog/set-disable-cat/<id>/", views.set_blog_cat_disable, name="admin_category_blog_set_active"),
]
