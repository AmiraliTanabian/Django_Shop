from datetime import datetime

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic import View, ListView

from contact_module.models import ContactModel
from news_module.models import Article, ArticleCategories, ArticleTag, ArticleComment
from product_module.models import Product
from site_module.models import SiteSetting, SiteBanners, Slider
from .forms import SettingEditForms, BannersEditForm, EditSliderForm, AdminContactForm, EditArticleForm, \
    AddArticleCatForm, AddArticleTagForm, EditCommentForms, EditProductForm


@login_required()
def index(request):
    if request.user.is_staff:
        return render(request, "admin_module/index.html")
    raise PermissionDenied


@permission_required(perm=['site_module.view_sitesetting', 'site_module.view_sitebanners', 'site_module.view_slider'],
                     raise_exception=True)
def main_setting_page(request):
    return render(request, "admin_module/settings/setting_main_page.html")


class MainSetting(PermissionRequiredMixin, View):
    permission_required = ["site_module.change_sitesetting", "site_module.view_sitesetting",
                           "site_module.add_sitesetting", "site_module.delete_sitesetting"]
    permission_denied_message = "شما به تغییر تنظیمات سایت دسترسی ندارید"

    def get(self, request: HttpRequest):
        current_settings = SiteSetting.objects.all().first()
        form = SettingEditForms(instance=current_settings)
        setting = current_settings
        return render(request, "admin_module/settings/settings_page.html", {
            "form": form,
            "setting": setting,
        })

    def post(self, request: HttpRequest):
        current_settings = SiteSetting.objects.all().first()
        form: SettingEditForms = SettingEditForms(request.POST, request.FILES, instance=current_settings)

        if form.is_valid():
            form.save()
            messages.success(request, "اطلاعات با موفقیت تغییر کرده است")
            return redirect(reverse_lazy('admin_setting_main_page'))
        return render(request, "admin_module/settings/settings_page.html", {
            "form": form
        })


class SettingsAdsView(PermissionRequiredMixin, ListView):
    model = SiteBanners
    paginate_by = 5
    context_object_name = "banners"
    template_name = "admin_module/settings/settings_ads.html"
    permission_required = ['site_module.view_sitebanners']
    permission_denied_message = "شما دسترسی به مشاهده تبلیغات سایت ندارید"


class AdsEditView(PermissionRequiredMixin, View):
    permission_required = ["site_module.add_sitebanners"]

    def get(self, request: HttpRequest, id):
        current_banner = get_object_or_404(SiteBanners, id=id)
        form = BannersEditForm(instance=current_banner)

        return render(request, "admin_module/settings/settings_edit_ads.html", {
            "form": form,
            "banner": current_banner,
        })

    def post(self, request: HttpRequest, id):
        current_banner = get_object_or_404(SiteBanners, id=id)
        form = BannersEditForm(request.POST, request.FILES, instance=current_banner)

        if form.is_valid():
            form.save()
            messages.success(request, "بنر با موفقیت تغییر کرده است")
            # return redirect(reverse_lazy('ads_edit_page'))
        return render(request, "admin_module/settings/settings_edit_ads.html", {
            "form": form,
            "banner": current_banner,
        })


class SliderListPage(PermissionRequiredMixin, ListView):
    template_name = "admin_module/settings/settings_sliders_list.html"
    context_object_name = "sliders"
    paginate_by = 5
    model = Slider
    permission_required = ["site_module.view_slider"]
    permission_denied_message = "شما دسترسی به دیدن اسلایدر ها ندارید"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_active=True)
        return query


class SliderDetailView(PermissionRequiredMixin, View):
    permission_required = [
        "site_module.view_slider",
        "site_module.change_slider",
        "site_module.delete_slider",
        "site_module.add_slider"
    ]
    permission_denied_message = "شما دسترسی به تغییر یا افزودن اسلایدر ندارید"

    def get(self, request: HttpRequest, id):
        current_slider = get_object_or_404(Slider, id=id)
        form = EditSliderForm(instance=current_slider)
        return render(request, "admin_module/settings/settings_slider_edit.html", {
            "form": form,
            "slider": current_slider
        })

    def post(self, request: HttpRequest, id):
        current_slider = get_object_or_404(Slider, id=id)
        form = EditSliderForm(request.POST, request.FILES, instance=current_slider)
        if form.is_valid():
            form.save()
            messages.success(request, "اسلایدر با موفقیت ویرایش شد")
        return render(request, "admin_module/settings/settings_slider_edit.html", {
            "form": form,
            "slider": current_slider
        })


class ContactUsListView(PermissionRequiredMixin, ListView):
    model = ContactModel
    paginate_by = 10
    template_name = "admin_module/contact-us/contact_us_list.html"
    context_object_name = "messages"
    permission_required = [
        'contact_module.view_contactmodel'
    ]
    permission_denied_message = "شما دسترسی به دیدن پیام ها ندارید"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.order_by("date")
        return query


class ContactUsDetailView(PermissionRequiredMixin, View):
    permission_required = [
        "contact_module.view_contactmodel",
        "contact_module.delete_contactmodel",
        "contact_module.change_contactmodel",
        "contact_module.add_contactmodel",
    ]
    permission_denied_message = "شما دسترسی به تغییرات در پیام های تماس با ما را ندارید"

    def get(self, request, id):
        current_obj = get_object_or_404(ContactModel, id=id)
        form = AdminContactForm(instance=current_obj)
        return render(request, "admin_module/contact-us/contact_us_edit.html", {
            "form": form,
            "contact_us": current_obj,
        })

    def post(self, request, id):
        current_obj = get_object_or_404(ContactModel, id=id)
        form = AdminContactForm(request.POST, request.FILES, instance=current_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "پیغام با موفقیت ویرایش شد")
        return render(request, "admin_module/contact-us/contact_us_edit.html", {
            "form": form,
            "contact_us": current_obj,
        })


@permission_required(perm=["contact_module.view_contactmodel",
                           "contact_module.delete_contactmodel",
                           "contact_module.change_contactmodel",
                           "contact_module.add_contactmodel", ], raise_exception=True)
def send_msg_answer_ajax(request: HttpRequest):
    answer = request.GET.get("answer")
    id = request.GET.get('id')
    contact_model = get_object_or_404(ContactModel, id=id)
    user_email = contact_model.email

    if not request.user.is_superuser:
        return JsonResponse({
            "status": "faild",
            "msg": "شما دسترسی به این کار را ندارید."
        })

    try:
        email_content = render_to_string("admin_module/contact-us/email_template.html", {
            "answer_text": answer
        })
        mail = EmailMessage(
            "پاسخ به پیام",
            email_content,
            "atanabain@gmail.com",
            [user_email],
        )
        mail.content_subtype = "html"
        mail.send()

        contact_model.is_read = True
        contact_model.answer_date = datetime.now()
        contact_model.answer = answer
        contact_model.save()

        return JsonResponse({
            "status": "failed!",
            "title": "انجام شد",
            "msg": 'پاسخ با موفقیت ایمیل شد ',
            "icon": "success"
        })

    except:
        return JsonResponse({
            "status": "failed!",
            "title": "خطا",
            "msg": 'ارسال ایمیل با مشکل مواجه شد \n لطفا دوباره تلاش کنید',
            "icon": "error"
        })


class BlogListView(PermissionRequiredMixin, ListView):
    paginate_by = 10
    model = Article
    template_name = "admin_module/blog/blog_list.html"
    context_object_name = "posts"
    permission_required = [
        "news_module.view_article",
    ]
    permission_denied_message = "شما دسترسی به دیدن لیست مقالات را ندارید"


class BlogEditPage(PermissionRequiredMixin, View):
    permission_required = [
        "news_module.view_article",
        "news_module.delete_article",
        "news_module.change_article",
        "news_module.add_article",
    ]
    permission_denied_message = "شما دسترسی به ایجاد تغییرات در مقالات را ندارید"

    def get(self, request: HttpRequest, id):
        current_post = get_object_or_404(Article, id=id)
        form = EditArticleForm(instance=current_post)
        return render(request, "admin_module/blog/blog_detail.html", {
            "form": form,
            "post": current_post,
        })

    def post(self, request: HttpRequest, id):
        current_post = get_object_or_404(Article, id=id)
        form = EditArticleForm(request.POST, request.FILES, instance=current_post)
        if form.is_valid():
            form.save()
            messages.success(request, "پست با موفقیت ویرایش شد")

        return render(request, "admin_module/blog/blog_detail.html", {
            "form": form,
            "post": current_post,
        })


class BlogAddPage(PermissionRequiredMixin, FormView):
    form_class = EditArticleForm
    template_name = "admin_module/blog/blog_add_post.html"
    permission_required = [
        "news_module.view_article",
        "news_module.delete_article",
        "news_module.change_article",
        "news_module.add_article",
    ]
    permission_denied_message = "شما دسترسی به ایجاد تغییرات در مقالات را ندارید"

    def form_valid(self, form):
        current_user = self.request.user
        form.instance.author = current_user
        form.save()
        messages.success(self.request, "پست شما با موفقیت افزوده شد")
        return redirect(reverse_lazy("admin_blog_list_page"))


class ArticleCategoriesList(PermissionRequiredMixin, ListView):
    model = ArticleCategories
    paginate_by = 10
    template_name = "admin_module/blog/admin_blog_category.html"
    context_object_name = "cats"
    permission_required = [
        "news_module.view_articlecategories",
    ]
    permission_denied_message = "شما دسترسی به مشاهده دسته بندی ها را ندارید"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.order_by("-id")
        return query


@permission_required(perm=["news_module.delete_articlecategories", ], raise_exception=True)
def remove_category_ajax(request: HttpRequest, id):
    try:
        current_category = get_object_or_404(ArticleCategories, id=id)
        current_category.delete()
        return JsonResponse({
            "title": "موفق",
            "msg": "دسته بندی با موفقیت حدف شد",
            "icon": "success",
        })

    except:
        return JsonResponse({
            "title": "خطا",
            "msg": "خطایی رخ داد.",
            "icon": "error",
        })


class AddArticleCategory(PermissionRequiredMixin, View):
    permission_required = [
        "news_module.view_articlecategories",
        "news_module.delete_articlecategories",
        "news_module.change_articlecategories",
        "news_module.add_articlecategories",
    ]
    permission_denied_message = "شما دسترسی به ایجاد تغییر در دسته بندی مقالات را ندارید"

    def get(self, request: HttpRequest):
        form = AddArticleCatForm()
        return render(request, "admin_module/blog/add_blog_cat.html", {
            "form": form
        })

    def post(self, request: HttpRequest):
        form = AddArticleCatForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "دسته بندی با موفقیت افزوده شد")
            return redirect(reverse_lazy("admin_blog_categories"))

        return render(request, "admin_module/blog/add_blog_cat.html", {
            "form": form
        })


@permission_required(perm=["news_module.change_articlecategories", ], raise_exception=True)
def set_blog_cat_active(request: HttpRequest, id):
    try:
        current_cat = get_object_or_404(ArticleCategories, id=id)
        current_cat.is_active = True
        current_cat.save()
        return JsonResponse({
            "title": "تغییر وضعیت دسته بندی",
            "msg": "دسته بندی با موفقیت فعال شد",
            "icon": "success",
        })

    except:
        return JsonResponse({
            "title": "تغییر وضعیت دسته بندی",
            "msg": "تغییر وضعیت دسته بندی با خطا مواجه شد",
            "icon": "error",
        })


@permission_required(perm=["news_module.change_articlecategories", ], raise_exception=True)
def set_blog_cat_disable(request: HttpRequest, id):
    try:
        current_cat = get_object_or_404(ArticleCategories, id=id)
        current_cat.is_active = False
        current_cat.save()
        return JsonResponse({
            "title": "تغییر وضعیت دسته بندی",
            "msg": "دسته بندی با موفقیت غیرفعال شد",
            "icon": "success",
        })

    except:
        return JsonResponse({
            "title": "تغییر وضعیت دسته بندی",
            "msg": "تغییر وضعیت دسته بندی با خطا مواجه شد",
            "icon": "error",
        })


class AdminBlogTagsList(PermissionRequiredMixin, ListView):
    model = ArticleTag
    paginate_by = 10
    template_name = "admin_module/blog/admin_blog_tags.html"
    context_object_name = "tags"
    permission_required = [
        "news_module.view_articletag"
    ]
    permission_denied_message = "شما دسترسی برای مشاهده تگ های مقالات را ندارید"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.order_by("-id")
        return query


@permission_required(
    perm=["news_module.delete_articletag"], raise_exception=True)
def remove_tag_ajax(request: HttpRequest, id):
    try:
        current_tag = get_object_or_404(ArticleTag, id=id)
        current_tag.delete()
        return JsonResponse({
            "title": "موفق",
            "msg": "تگ با موفقیت حدف شد",
            "icon": "success",
        })

    except Exception as Error:
        print(Error)
        return JsonResponse({
            "title": "خطا",
            "msg": "خطایی رخ داد.",
            "icon": "error",
        })


@permission_required(
    perm=["news_module.view_articletag", "news_module.delete_articletag", "news_module.change_articletag",
          "news_module.add_articletag"], raise_exception=True)
def set_blog_tag_active(request: HttpRequest, id):
    try:
        current_tag = get_object_or_404(ArticleTag, id=id)
        current_tag.is_active = True
        current_tag.save()
        return JsonResponse({
            "title": "تغییر وضعیت تگ",
            "msg": " تگ با موفقیت فعال شد",
            "icon": "success",
        })

    except:
        return JsonResponse({
            "title": "تغییر وضعیت تگ",
            "msg": "تغییر وضعیت تگ با خطا مواجه شد",
            "icon": "error",
        })


@permission_required(
    perm=["news_module.view_articletag", "news_module.delete_articletag", "news_module.change_articletag",
          "news_module.add_articletag"], raise_exception=True)
def set_blog_tag_disable(request: HttpRequest, id):
    try:
        current_tag = get_object_or_404(ArticleTag, id=id)
        current_tag.is_active = False
        current_tag.save()
        return JsonResponse({
            "title": "تغییر وضعیت تگ",
            "msg": " تگ با موفقیت فعال شد",
            "icon": "success",
        })

    except:
        return JsonResponse({
            "title": "تغییر وضعیت تگ",
            "msg": "تغییر وضعیت تگ با خطا مواجه شد",
            "icon": "error",
        })


class AddArticleTag(PermissionRequiredMixin, View):
    permission_required = [
        "news_module.view_articletag",
        "news_module.delete_articletag",
        "news_module.change_articletag",
        "news_module.add_articletag",
    ]
    permission_denied_message = "شما دسترسی به ایجاد تغییرات در تگ مقالات را ندارید"

    def get(self, request: HttpRequest):
        form = AddArticleTagForm()
        return render(request, "admin_module/blog/add_blog_tag.html", {
            "form": form
        })

    def post(self, request: HttpRequest):
        form = AddArticleTagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تگ با موفقیت افزوده شد")
            return redirect(reverse_lazy("admin_blog_tags"))

        return render(request, "admin_module/blog/add_blog_tag.html", {
            "form": form
        })


class BlogPostCommentList(PermissionRequiredMixin, ListView):
    model = ArticleComment
    paginate_by = 10
    context_object_name = "comments"
    template_name = "admin_module/blog/blog_post_comments.html"
    permission_required = [
        "news_module.view_articlecomment"
    ]
    permission_denied_message = "شما دسترسی برای مشاهده نظرات مقالات را ندارید"

    def get_queryset(self, *args, **kwargs):
        query = super().get_queryset(*args, **kwargs)
        current_article = get_object_or_404(Article, id=self.kwargs.get('post_id'))
        query = query.filter(article=current_article).order_by("-id")
        return query


class PostCommentDetail(PermissionRequiredMixin, View):
    permission_required = [
        "news_module.view_articlecomment"
        "news_module.delete_articlecomment"
        "news_module.change_articlecomment"
        "news_module.add_articlecomment"
    ]
    permission_denied_message = "شما دسترسی برای ایجاد تغییرات در نظرات مقالات را ندارید"

    def get(self, request, comment_id):
        form = EditCommentForms()
        current_comment = get_object_or_404(ArticleComment, id=comment_id)
        return render(request, "admin_module/blog/blog_comment_detail.html", {
            "form": form,
            "comment": current_comment,
        })

    def post(self, request, comment_id):
        form = EditCommentForms(request.POST)
        current_comment = get_object_or_404(ArticleComment, id=comment_id)
        if form.is_valid():
            comment_status = form.cleaned_data.get("status")
            current_comment.status = comment_status
            current_comment.save()

            messages.success(request, "کامنت مورد نظر با موفقیت ویرایش شد")
            return redirect(reverse_lazy("admin_blog_post_comments", args=[current_comment.article.id]))

        return render(request, "admin_module/blog/blog_comment_detail.html", {
            "form": form,
            "comment": current_comment,
        })


def admin_logout(request: HttpRequest):
    if request.user:
        logout(request)
        messages.success(request, "ادمین عزیز شما خارج شدید")
    return redirect(reverse_lazy('login_page'))


class ProductsListView(PermissionRequiredMixin, ListView):
    paginate_by = 10
    model = Product
    template_name = "admin_module/products/products_list.html"
    context_object_name = "products"
    permission_required = [
        "product_module.view_product",
    ]
    permission_denied_message = "شما دسترسی به دیدن لیست محصولات را ندارید"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.order_by("-id")
        return query


class ProductEditView(PermissionRequiredMixin, View):
    context_object_name = "products"
    permission_required = [
        "product_module.change_product",
    ]

    def get(self, request: HttpRequest, id):
        product = get_object_or_404(Product, id=id)
        form = EditProductForm(instance=product)
        return render(request, "admin_module/products/product_detail.html", {
            "form": form,
            "product": product
        })

    def post(self, request: HttpRequest, id):
        product = get_object_or_404(Product, id=id)
        form = EditProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "محصول مورد نظر با موفقیت ویرایش")
        return render(request, "admin_module/products/product_detail.html", {
            "form": form,
            "product": product
        })


class AddProductView(PermissionRequiredMixin, View):
    permission_required = [
        "product_module.add_product"
    ]
    permission_denied_message = "شما دسترسی افزودن کالا را ندارید"

    def get(self, request: HttpRequest):
        form = EditProductForm()
        return render(request, "admin_module/products/add_product.html", {
            "form": form,
        })

    def post(self, request: HttpRequest):
        form = EditProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "محصول مورد نظر با موفقیت افزوده شد")
            return redirect(reverse_lazy("admin_products_list"))
        return render(request, "admin_module/products/add_product.html", {
            "form": form,
        })
