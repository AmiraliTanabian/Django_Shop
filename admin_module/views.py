from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import EmailMessage
from django.db.models import Count
from django.db.models.aggregates import Sum
from django.db.models.expressions import F
from django.http import Http404
from django.http import HttpRequest
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic import View, ListView, TemplateView

from contact_module.models import ContactModel
from news_module.models import Article, ArticleCategories, ArticleTag, ArticleComment
from newsletter_module.models import newsLetterModel
from order_module.models import orderModel, orderProductModel, orderStatus
from product_module.models import Product, ProductCategory, ProductTag, ProductComment, Brand, ProductGallery
from site_module.models import SiteSetting, SiteBanners, Slider
from user_profile_module.models import ticket_model, UnitsChoices, TicketAnswerModel, ticket_attachment
from .forms import SettingEditForms, BannersEditForm, EditSliderForm, AdminContactForm, EditArticleForm, \
    AddArticleCatForm, AddArticleTagForm, EditCommentForms, EditProductForm, AddProductCatForm, AddProductTagForm, \
    EditProductCommentForm, AddProductBrandForm, EditOrder, UserEditForm, SendTicketReplyForm, TicketUnitUpdateForm


class HomePageView(TemplateView):
    template_name = "admin_module/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_orders = orderModel.objects.filter(is_paid=True).order_by("-id")[:10]
        unread_tickets = ticket_model.objects.filter(has_unread_reply=True).order_by("-id")[:10]
        total_sales = orderProductModel.objects.filter(order__is_paid=True).aggregate(
            total=Sum(F("count") * F("finally_price"))
        )

        # Get last month total sales
        this_month_start_day = datetime.now().replace(day=1)
        this_month_end_day = this_month_start_day + relativedelta(months=1)
        total_this_month_sales = orderProductModel.objects.filter(order__is_paid=True,
                                                                  order__paid_date__gte=this_month_start_day,
                                                                  order__paid_date__lt=this_month_end_day).aggregate(
            total=Sum(F("count") * F("finally_price"))
        )

        # users stats
        total_users_count = get_user_model().objects.all().count()
        total_user_this_month = get_user_model().objects.filter(account_activation_date__gte=this_month_start_day,
                                                                account_activation_date__lt=this_month_end_day,
                                                                account_activated=True).count()
        total_user_this_month_percent = int((total_user_this_month / total_users_count) * 100)

        paid_orders = orderModel.objects.filter(is_paid=True)
        total_paid_orders = paid_orders.count()
        paid_order_counts = {
            item["status"]: item["count"]
            for item in paid_orders.values("status").annotate(count=Count("id"))
        }
        status_badges = ["blue", "pink", "palegreen", "yellow", "red", "orange"]
        order_status_stats = []
        for index, (status, label) in enumerate(orderStatus.choices):
            count = paid_order_counts.get(status, 0)
            percentage = round((count / total_paid_orders) * 100) if total_paid_orders else 0
            order_status_stats.append({
                "label": label,
                "count": count,
                "percentage": percentage,
                "badge": status_badges[index],
            })

        most_sells_product = Product.objects.filter(is_active=True).order_by("-order_count")[:10]

        # get product stats according stock
        all_active_products = Product.objects.filter(is_active=True)
        out_of_stock_products = all_active_products.filter(count=0)
        low_stock_products = all_active_products.filter(count__lte=10)
        enough_stack_products_count = all_active_products.count() - low_stock_products.count() - out_of_stock_products.count()

        total_products_count = Product.objects.count()
        inactive_products_count = total_products_count - all_active_products.count()
        active_products_percent = int(
            (all_active_products.count() / total_products_count) * 100) if total_products_count else 0
        inactive_products_percent = int(
            (inactive_products_count / total_products_count) * 100) if total_products_count else 0

        context["last_orders"] = last_orders
        context["unread_tickets"] = unread_tickets
        context["total_sales"] = total_sales["total"] or 0
        context["total_this_month_sales"] = total_this_month_sales["total"] or 0
        context["total_users_count"] = total_users_count
        context["total_user_this_month"] = total_user_this_month
        context["total_user_this_month_percent"] = total_user_this_month_percent
        context["order_status_stats"] = order_status_stats
        context["most_sells_product"] = most_sells_product

        context["all_active_products_count"] = all_active_products.count()
        context["out_of_stock_products_count"] = out_of_stock_products.count()
        context["out_of_stock_products_percent"] = int(
            (out_of_stock_products.count() / all_active_products.count()) * 100)
        context["low_stock_products_count"] = low_stock_products.count()
        context["low_stock_products_percent"] = int((low_stock_products.count() / all_active_products.count()) * 100)
        context["enough_stack_products_count"] = enough_stack_products_count
        context["enough_stack_products_count_percent"] = int(
            (enough_stack_products_count / all_active_products.count()) * 100)
        context["total_products_count"] = total_products_count
        context["active_products_percent"] = active_products_percent
        context["inactive_products_count"] = inactive_products_count
        context["inactive_products_percent"] = inactive_products_percent
        return context


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
        current_comment = get_object_or_404(ArticleComment, id=comment_id)
        form = EditCommentForms(instance=current_comment)
        return render(request, "admin_module/blog/blog_comment_detail.html", {
            "form": form,
            "comment": current_comment,
        })

    def post(self, request, comment_id):
        current_comment = get_object_or_404(ArticleComment, id=comment_id)
        form = EditCommentForms(request.POST, instance=current_comment)
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
        galleries = ProductGallery.objects.filter(product=product)
        form = EditProductForm(instance=product)
        return render(request, "admin_module/products/product_detail.html", {
            "form": form,
            "product": product,
            "galleries": galleries
        })

    def post(self, request: HttpRequest, id):
        product = get_object_or_404(Product, id=id)
        form = EditProductForm(request.POST, instance=product)
        galleries = ProductGallery.objects.filter(product=product)

        if form.is_valid():
            form.save()
            messages.success(request, "محصول مورد نظر با موفقیت ویرایش شد")
        return render(request, "admin_module/products/product_detail.html", {
            "form": form,
            "product": product,
            "galleries": galleries
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


class ProductCategoriesList(PermissionRequiredMixin, ListView):
    model = ProductCategory
    paginate_by = 10
    template_name = "admin_module/products/product_categories_list.html"
    context_object_name = "cats"
    permission_required = [
        "product_module.view_productcategory",
    ]
    permission_denied_message = "شما دسترسی به مشاهده دسته بندی ها را ندارید"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.order_by("-id")
        return query


@permission_required(perm=["product_module.delete_productcategory", ], raise_exception=True)
def remove_product_category_ajax(request: HttpRequest, id):
    try:
        current_category = get_object_or_404(ProductCategory, id=id)
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


@permission_required(
    perm=["product_module.change_productcategory"], raise_exception=True)
def set_product_cat_active(request: HttpRequest, id):
    try:
        current_category = get_object_or_404(ProductCategory, id=id)
        current_category.is_active = True
        current_category.save()
        return JsonResponse({
            "title": "تغییر وضعیت دسته بندی",
            "msg": " دسته بندی با موفقیت فعال شد",
            "icon": "success",
        })

    except:
        return JsonResponse({
            "title": "تغییر وضعیت دسته بندی",
            "msg": "تغییر وضعیت دسته بندی با خطا مواجه شد",
            "icon": "error",
        })


@permission_required(
    perm=["product_module.change_productcategory"], raise_exception=True)
def set_product_cat_disable(request: HttpRequest, id):
    try:
        current_category = get_object_or_404(ProductCategory, id=id)
        current_category.is_active = False
        current_category.save()
        return JsonResponse({
            "title": "تغییر وضعیت تگ",
            "msg": " تگ با موفقیت غیرفعال شد",
            "icon": "success",
        })

    except:
        return JsonResponse({
            "title": "تغییر وضعیت تگ",
            "msg": "تغییر وضعیت تگ با خطا مواجه شد",
            "icon": "error",
        })


class AddProductCategory(PermissionRequiredMixin, View):
    permission_required = [
        "product_module.add_productcategory"
    ]
    permission_denied_message = "شما دسترسی به ایجاد دسته بندی محصولات را ندارید"

    def get(self, request: HttpRequest):
        form = AddProductCatForm()
        return render(request, "admin_module/products/add_product_cat.html", {
            "form": form
        })

    def post(self, request: HttpRequest):
        form = AddProductCatForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "دسته بندی با موفقیت افزوده شد")
            return redirect(reverse_lazy("admin_product_categories_list"))

        return render(request, "admin_module/products/add_product_cat.html", {
            "form": form
        })


class AdminProductTagsList(PermissionRequiredMixin, ListView):
    model = ProductTag
    paginate_by = 10
    template_name = "admin_module/products/product_tag_list.html"
    context_object_name = "tags"
    permission_required = [
        "product_module.view_producttag"
    ]
    permission_denied_message = "شما دسترسی برای مشاهده تگ های محصولات را ندارید"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.order_by("-id")
        return query


@permission_required(
    perm=["product_module.delete_producttag"], raise_exception=True)
def remove_product_tag_ajax(request: HttpRequest, id):
    try:
        current_tag = get_object_or_404(ProductTag, id=id)
        current_tag.delete()
        return JsonResponse({
            "title": "موفق",
            "msg": "تگ با موفقیت حدف شد",
            "icon": "success",
        })

    except:
        return JsonResponse({
            "title": "خطا",
            "msg": "خطایی رخ داد.",
            "icon": "error",
        })


@permission_required(
    perm=['product_module.change_producttag'], raise_exception=True)
def set_product_tag_active(request: HttpRequest, id):
    try:
        current_tag = get_object_or_404(ProductTag, id=id)
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
    perm=["product_module.change_producttag"], raise_exception=True)
def set_product_tag_disable(request: HttpRequest, id):
    try:
        current_tag = get_object_or_404(ProductTag, id=id)
        current_tag.is_active = False
        current_tag.save()
        return JsonResponse({
            "title": "تغییر وضعیت تگ",
            "msg": " تگ با موفقیت غیرفعال شد",
            "icon": "success",
        })

    except:
        return JsonResponse({
            "title": "تغییر وضعیت تگ",
            "msg": "تغییر وضعیت تگ با خطا مواجه شد",
            "icon": "error",
        })


class AddProductTag(PermissionRequiredMixin, View):
    permission_required = [
        "product_module.add_producttag"
    ]
    permission_denied_message = "شما دسترسی به ایجاد   تگ محصولات را ندارید"

    def get(self, request: HttpRequest):
        form = AddProductTagForm()
        return render(request, "admin_module/products/add_product_tag.html", {
            "form": form
        })

    def post(self, request: HttpRequest):
        form = AddProductTagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تگ با موفقیت افزوده شد")
            return redirect(reverse_lazy("admin_product_tags_list"))

        return render(request, "admin_module/products/add_product_tag.html", {
            "form": form
        })


@permission_required(perm=["product_module.delete_product"], raise_exception=True)
def remove_product_ajax(request: HttpRequest, id):
    try:
        current_product = get_object_or_404(Product, id=id)
        current_product.delete()
        return JsonResponse({
            "title": "موفق",
            "msg": "محصول با موفقیت حدف شد",
            "icon": "success",
        })

    except:
        return JsonResponse({
            "title": "خطا",
            "msg": "خطایی رخ داد.",
            "icon": "error",
        })


class ProductCommentList(PermissionRequiredMixin, ListView):
    model = ProductComment
    paginate_by = 10
    context_object_name = "comments"
    template_name = "admin_module/products/product_comments_list.html"
    permission_required = [
        "product_module.view_productcomment"
    ]
    permission_denied_message = "شما دسترسی برای مشاهده نظرات محصول را ندارید"

    def get_queryset(self, *args, **kwargs):
        query = super().get_queryset(*args, **kwargs)
        current_product = get_object_or_404(Product, id=self.kwargs.get('product_id'))
        query = query.filter(product=current_product).order_by("-id")
        return query

    def get_context_data(self, *args, **kwargs):
        current_product = get_object_or_404(Product, id=self.kwargs.get('product_id'))
        context = super().get_context_data(*args, **kwargs)
        context["product"] = current_product
        return context


class ProductCommentDetail(PermissionRequiredMixin, View):
    permission_required = [
        "product_module.change_productcomment"
    ]
    permission_denied_message = "شما دسترسی برای ایجاد تغییرات در نظرات محصولات را ندارید"

    def get(self, request, comment_id):
        current_comment = get_object_or_404(ProductComment, id=comment_id)
        form = EditProductCommentForm(instance=current_comment)
        score_range = range(current_comment.score)
        return render(request, "admin_module/products/product_comment_detail.html", {
            "form": form,
            "comment": current_comment,
            "score_range": score_range,
        })

    def post(self, request, comment_id):
        current_comment = get_object_or_404(ProductComment, id=comment_id)
        form = EditProductCommentForm(request.POST, instance=current_comment)
        score_range = range(current_comment.score)

        if form.is_valid():
            comment_status = form.cleaned_data.get("status")
            current_comment.status = comment_status
            current_comment.save()

            messages.success(request, "کامنت مورد نظر با موفقیت ویرایش شد")
            return redirect(reverse_lazy("admin_product_comments", args=[current_comment.product.id]))

        return render(request, "admin_module/products/product_comment_detail.html", {
            "form": form,
            "comment": current_comment,
            "score_range": score_range
        })


class ProductBrandList(PermissionRequiredMixin, ListView):
    paginate_by = 10
    model = Brand
    template_name = "admin_module/products/product_brands_list.html"
    context_object_name = "brands"
    permission_required = [
        "product_module.view_brand",
    ]
    permission_denied_message = "شما دسترسی به دیدن لیست برند محصولات را ندارید"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.order_by("-id")
        return query


@permission_required(perm=["product_module.delete_brand"], raise_exception=True)
def remove_product_brand_ajax(request: HttpRequest, id):
    try:
        current_brand = get_object_or_404(Brand, id=id)
        current_brand.delete()
        return JsonResponse({
            "title": "موفق",
            "msg": "برند با موفقیت حدف شد",
            "icon": "success",
        })

    except:
        return JsonResponse({
            "title": "خطا",
            "msg": '''
            خظایی رخ داد 
            ( توجه کنید نمیتوانید برند هایی که محصولی برای آنها ثبت شده است را حذف کنید )
            ''',
            "icon": "error",
        })


@permission_required(
    perm=["product_module.change_brand"], raise_exception=True)
def set_product_brand_active(request: HttpRequest, id):
    try:
        current_brand = get_object_or_404(Brand, id=id)
        current_brand.is_active = True
        current_brand.save()
        return JsonResponse({
            "title": "تغییر برند",
            "msg": " برند با موفقیت فعال شد",
            "icon": "success",
        })

    except:
        return JsonResponse({
            "title": "تغییر وضعیت برند",
            "msg": "تغییر وضعیت برند با خطا مواجه شد",
            "icon": "error",
        })


@permission_required(
    perm=["product_module.change_brand"], raise_exception=True)
def set_product_brand_disable(request: HttpRequest, id):
    try:
        current_brand = get_object_or_404(Brand, id=id)
        current_brand.is_active = False
        current_brand.save()
        return JsonResponse({
            "title": "تغییر وضعیت برند",
            "msg": " برند با موفقیت فعال شد",
            "icon": "success",
        })

    except:
        return JsonResponse({
            "title": "تغییر وضعیت برند",
            "msg": "تغییر وضعیت برند با خطا مواجه شد",
            "icon": "error",
        })


class AddProductBrand(PermissionRequiredMixin, View):
    permission_required = [
        "product_module.add_brand"
    ]
    permission_denied_message = "شما دسترسی به ایجاد برند محصولات را ندارید"

    def get(self, request: HttpRequest):
        form = AddProductBrandForm()
        return render(request, "admin_module/products/add_product_brand.html", {
            "form": form
        })

    def post(self, request: HttpRequest):
        form = AddProductBrandForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "برند با موفقیت افزوده شد")
            return redirect(reverse_lazy("admin_product_brands"))

        return render(request, "admin_module/products/add_product_brand.html", {
            "form": form
        })


@permission_required(perm=["product_module.delete_productgallery"], raise_exception=True)
def remove_product_gallery_ajax(request: HttpRequest, id):
    try:
        product_gallery = get_object_or_404(ProductGallery, id=id)
        product_gallery.delete()

        return JsonResponse({
            "status": "ok",
        })

    except:
        return JsonResponse({
            "status": "error",
            "title": "حدف گالری محصول",
            "msg": "حذف با خطا مواجه شد",
            "icon": "error",
        })


@permission_required(perm=["product_module.add_productgallery"], raise_exception=True)
def add_product_gallery_ajax(request: HttpRequest):
    if request.method == "GET":
        return JsonResponse({
            "success": False,
            "msg": "درخواست نامعتبر"
        })
    # get file and create product banner
    file = request.FILES["file"]
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, id=product_id)
    product_gallery = ProductGallery(product=product, banner=file)
    product_gallery.save()

    return JsonResponse({
        "success": True,
        "msg": "گالری محصول با موفقیت افزوده شد",
    })


class OrderList(PermissionRequiredMixin, ListView):
    paginate_by = 10
    model = orderModel
    template_name = "admin_module/order/order_list.html"
    context_object_name = "orders"
    permission_required = [
        "order_module.view_ordermodel"
    ]
    permission_denied_message = "شما دسترسی به مشاهده لیست سفارش ها را ندارید"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_paid=True).order_by("-id")
        return query


class OrderDetailView(PermissionRequiredMixin, View):
    permission_required = [
        'order_module.change_ordermodel'
    ]
    permission_denied_message = "شما دسترسی برای ایجاد تغییرات در سفارش ها را ندارید"

    def get(self, request, order_id):
        current_order = get_object_or_404(orderModel, id=order_id)
        form = EditOrder(instance=current_order)
        order_products = orderProductModel.objects.filter(order=current_order)
        return render(request, "admin_module/order/order_detail.html", {
            "form": form,
            "order": current_order,
            "products": order_products,
        })

    def post(self, request, order_id):
        current_order = get_object_or_404(orderModel, id=order_id)
        form = EditOrder(request.POST, instance=current_order)
        order_products = orderProductModel.objects.filter(order=current_order)

        if form.is_valid():
            order_status = form.cleaned_data.get("status")
            current_order.status = order_status
            current_order.save()

            messages.success(request, "سفارش مورد نظر با موفقیت ویرایش شد")
            return redirect(reverse_lazy("admin_order_list_page"))

        return render(request, "admin_module/order/order_detail.html", {
            "form": form,
            "comment": current_order,
            "products": order_products,
        })


class UserListView(PermissionRequiredMixin, ListView):
    model = get_user_model()
    paginate_by = 10
    template_name = "admin_module/user/user_list.html"
    context_object_name = "users"
    permission_required = [
        "auth_module.view_user",
    ]
    permission_denied_message = "شما دسترسی به مشاهده لیست کاربران را ندارید"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.order_by("-id")
        return query


class UserEditView(PermissionRequiredMixin, View):
    permission_required = [
        "auth_module.view_user",
        "auth_module.change_user",
    ]
    permission_denied_message = "شما دسترسی به ویرایش لیست کاربران را ندارید"

    def get(self, request: HttpRequest, id):
        user = get_object_or_404(get_user_model(), id=id)
        form = UserEditForm(instance=user)
        user_orders = orderModel.objects.filter(user=user)
        return render(request, "admin_module/user/user_detail.html", {
            "form": form,
            "user": user,
            "orders": user_orders,
        })

    def post(self, request: HttpRequest, id):
        user = get_object_or_404(get_user_model(), id=id)
        form = UserEditForm(request.POST, request.FILES, instance=user)
        user_orders = orderModel.objects.filter(user=user)
        if form.is_valid():
            form.save()
            messages.success(request, "کاربر با موفقیت ویرایش شد")

        return render(request, "admin_module/user/user_detail.html", {
            "form": form,
            "user": user,
            "orders": user_orders,
        })


@permission_required(perm=["auth_module.change_user"], raise_exception=True)
def set_user_active(request: HttpRequest, id):
    try:
        user = get_object_or_404(get_user_model(), id=id)
        user.is_active = True
        user.save()
        return JsonResponse({
            "success": True,
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": e
        })


@permission_required(perm=["auth_module.change_user"], raise_exception=True)
def set_user_disable(request: HttpRequest, id):
    try:
        user = get_object_or_404(get_user_model(), id=id)
        user.is_active = False
        user.save()
        return JsonResponse({
            "success": True,
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": e
        })


class NewsLettersListView(PermissionRequiredMixin, ListView):
    model = newsLetterModel
    paginate_by = 20
    context_object_name = "newsLetters"
    template_name = "admin_module/newsLetter/newsLetter_list.html"
    permission_required = [
        "newsletter_module.view_newslettermodel"
    ]
    permission_denied_message = "شما دسترسی به مشاهده لیست خبرنامه را ندارید"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.order_by("-id")
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_newsletters = newsLetterModel.objects.all()
        count_of_newsletters = all_newsletters.count()
        count_of_active = all_newsletters.filter(is_active=True).count()
        count_of_disable = count_of_newsletters - count_of_active
        active_percent = (count_of_active / count_of_newsletters) * 100
        disable_percent = (count_of_disable / count_of_newsletters) * 100

        context["count_of_newsletter"] = count_of_newsletters
        context["count_of_active_newsletter"] = count_of_active
        context["count_of_disable_newsletter"] = count_of_disable
        context["active_percent"] = int(active_percent)
        context["disable_percent"] = int(disable_percent)

        return context


class TicketListView(PermissionRequiredMixin, ListView):
    model = ticket_model
    paginate_by = 20
    context_object_name = "tickets"
    template_name = "admin_module/tickets/ticket_list.html"
    permission_required = [
        "user_profile_module.view_ticket_model"
    ]
    permission_denied_message = "شما دسترسی به مشاهده لیست تیکت ها را ندارید"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.order_by("-id")
        return query

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        units = UnitsChoices.choices
        context['units'] = units
        return context


class UnitTicketView(PermissionRequiredMixin, ListView):
    model = ticket_model
    paginate_by = 20
    context_object_name = "tickets"
    template_name = "admin_module/tickets/tickets_unit_list.html"
    permission_required = [
        "user_profile_module.view_ticket_model"
    ]
    permission_denied_message = "شما دسترسی به مشاهده لیست تیکت ها را ندارید"

    def get_queryset(self):
        try:
            unit = UnitsChoices(self.kwargs["unit"])
        except ValueError:
            raise Http404

        query = super().get_queryset().filter(Unit=unit)
        query = query.order_by("-id")
        return query

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        units = UnitsChoices.choices

        current_unit = UnitsChoices(self.kwargs["unit"])
        unit_persian_lbl = current_unit.label

        context['units'] = units
        context["user_unit_persian"] = unit_persian_lbl
        context["user_unit_english"] = current_unit.value

        return context


class TicketDetail(PermissionRequiredMixin, View):
    permission_required = [
        "user_profile_module.change_ticket_model",
    ]
    permission_denied_message = "شما دسترسی به تغییر تیکت را ندارید"

    def get(self, request: HttpRequest, id):
        current_ticket = get_object_or_404(ticket_model, id=id)
        if current_ticket.has_unread_reply:
            current_ticket.has_unread_reply = False
            current_ticket.save(update_fields=["has_unread_reply"])
        ticket_answers = TicketAnswerModel.objects.filter(ticket=current_ticket)
        files = ticket_attachment.objects.filter(ticket=current_ticket)
        ticket_unit_lbl = UnitsChoices(current_ticket.Unit).label
        form = SendTicketReplyForm()
        unit_form = TicketUnitUpdateForm(instance=current_ticket)

        return render(request, "admin_module/tickets/ticket_detial.html", {
            "form": form,
            "ticket": current_ticket,
            "replies": ticket_answers,
            "files": files,
            "ticket_unit_lbl": ticket_unit_lbl,
            "unit_form": unit_form,
        })

    def post(self, request: HttpRequest, id):
        current_ticket = get_object_or_404(ticket_model, id=id)
        ticket_answers = TicketAnswerModel.objects.filter(ticket=current_ticket)
        files = ticket_attachment.objects.filter(ticket=current_ticket)
        ticket_unit_lbl = UnitsChoices(current_ticket.Unit).label
        form = SendTicketReplyForm(request.POST)
        unit_form = TicketUnitUpdateForm(instance=current_ticket)

        if form.is_valid():
            reply_text = form.cleaned_data.get("text")
            TicketAnswerModel.objects.create(
                text=reply_text,
                ticket=current_ticket,
                user=request.user
            )

            messages.success(request, "پاسخ تیکت با موفقیت ارسال شد")
            form = SendTicketReplyForm()

        return render(request, "admin_module/tickets/ticket_detial.html", {
            "form": form,
            "ticket": current_ticket,
            "replies": ticket_answers,
            "files": files,
            "ticket_unit_lbl": ticket_unit_lbl,
            "unit_form": unit_form,
        })


class TicketUnitUpdateView(PermissionRequiredMixin, View):
    permission_required = ["user_profile_module.change_ticket_model"]
    permission_denied_message = "شما دسترسی به تغییر واحد تیکت را ندارید"

    def post(self, request: HttpRequest, id):
        current_ticket = get_object_or_404(ticket_model, id=id)
        form = TicketUnitUpdateForm(request.POST, instance=current_ticket)

        if form.is_valid():
            form.save()
            messages.success(request, "واحد مربوط به تیکت با موفقیت تغییر کرد")
        else:
            messages.error(request, "واحد انتخاب‌شده معتبر نیست")

        return redirect("admin_ticket_detail_view", id=id)


@permission_required(perm=["user_profile_module.change_ticket_model"], raise_exception=True)
def set_ticket_close(request: HttpRequest, id):
    if request.method == "GET":
        try:
            current_ticket = get_object_or_404(ticket_model, id=id)

            # msg when ticket was closed
            if current_ticket.is_closed:
                return JsonResponse({
                    "success": False,
                    "title": "بسته شدن تیکت",
                    "icon": "warning",
                    "msg": "تیکت قبل از درخواست شما بسته شده بود"
                })
            current_ticket.is_closed = True
            current_ticket.save()
            return JsonResponse({
                "success": True,
                "title": "بسته شدن تیکت",
                "icon": "success",
                "msg": "تیکت با موفقیت بسته شد"
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "title": "بسته شدن تیکت",
                "icon": "error",
                "msg": "بسته شدن تیکت با ارر مواجه شد \n لطفا بعدا تلاش کنید"
            })

    # POST
    else:
        return JsonResponse({
            "success": False,
            "title": "بسته شدن تیکت",
            "icon": "error",
            "msg": "درخواست نامعتبر"
        })
