from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
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
from news_module.models import Article
from site_module.models import SiteSetting, SiteBanners, Slider
from .forms import SettingEditForms, BannersEditForm, EditSliderForm, AdminContactForm, EditArticleForm


# Create your views here.
def index(request):
    return render(request, "admin_module/index.html")


def main_setting_page(request):
    return render(request, "admin_module/settings/setting_main_page.html")


class MainSetting(View):
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


class SettingsAdsView(LoginRequiredMixin, ListView):
    model = SiteBanners
    paginate_by = 5
    context_object_name = "banners"
    template_name = "admin_module/settings/settings_ads.html"


class AdsEditView(View):
    def get(self, request: HttpRequest, id):
        print("View start")
        current_banner = get_object_or_404(SiteBanners, id=id)
        form = BannersEditForm(instance=current_banner)
        print("View End")

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


class SliderListPage(ListView):
    template_name = "admin_module/settings/settings_sliders_list.html"
    context_object_name = "sliders"
    paginate_by = 5
    model = Slider

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_active=True)
        return query


class SliderDetailView(View):
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


class ContactUsListView(ListView):
    model = ContactModel
    paginate_by = 10
    template_name = "admin_module/contact-us/contact_us_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.order_by("date")
        return query


class ContactUsDetailView(View):
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


class BlogListView(ListView):
    paginate_by = 10
    model = Article
    template_name = "admin_module/blog/blog_list.html"
    context_object_name = "posts"


class BlogEditPage(View):
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


class BlogAddPage(FormView):
    form_class = EditArticleForm
    template_name = "admin_module/blog/blog_add_post.html"

    def form_valid(self, form):
        current_user = self.request.user
        form.instance.author = current_user
        form.save()
        messages.success(self.request, "پست شما با موفقیت افزوده شد")
        return redirect(reverse_lazy("admin_blog_list_page"))
