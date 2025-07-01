import re

from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView

from contact_module.models import ContactModel
from news_module.models import Article
from site_module.models import Slider, SiteSetting, SiteBanners
from .forms import ArticleEditForm, SliderDetailsForm, SiteSettingsForm, BannerEditForm


def index_page(request: HttpRequest):
    return render(request, "admin_panel_module/index.html")


class ArticlePageView(ListView):
    template_name = 'admin_panel_module/articles.html'
    context_object_name = "articles"
    paginate_by = 10
    model = Article


class EditArticleView(View):
    def get(self, request: HttpRequest, pk):
        current_article = get_object_or_404(Article, pk=int(pk))

        form = ArticleEditForm(instance=current_article)

        return render(request, "admin_panel_module/article_detail.html", {
            "form": form,
            "article": current_article,
        })

    def post(self, request: HttpRequest, pk):
        current_article = get_object_or_404(Article, pk=int(pk))

        form = ArticleEditForm(instance=current_article)

        print(f"Post log: {request.POST}")

        return render(request, "admin_panel_module/article_detail.html", {
            "form": form,
            "article": current_article,
        })


class ContactUSAdminView(ListView):
    ordering = ["-date"]
    model = ContactModel
    context_object_name = 'messages'
    paginate_by = 10
    template_name = 'admin_panel_module/messages_list.html'


class MessageDetailView(View):
    def get(self, request, pk):
        # Set msg to read
        obj = ContactModel.objects.filter(pk=pk).first()
        obj.is_read = True
        obj.save()

        return render(request, 'admin_panel_module/message_detail.html', {
            "msg": obj,
        })


class RemoveMessageAdminView(View):
    def get(self, request):
        msg_id = request.GET["msg_id"]
        msg = ContactModel.objects.filter(pk=msg_id).first()
        if not msg:
            return JsonResponse({
                "status": "failed",
                "msg": "the msg id not found!"
            })

        else:
            msg.delete()
            return JsonResponse({
                "status": "success",
            })


class SendMsgAnswer(View):
    def get(self, request):
        email = request.GET.get("email")
        cleaned_email = re.sub(r'[\s\r\n\t]', '', email)
        text = request.GET.get("text")

        mail_template = text
        mail = EmailMessage(
            "پاسخ به پیام شما",
            mail_template,
            'atanabain@gmail.com',
            [cleaned_email]
        )

        try:
            mail.send()
            return JsonResponse({
                "status": "success",
            })

        except Exception as Error:
            return JsonResponse(
                {
                    "status": "Error",
                    "msg": Error
                }
            )


class sliderList(ListView):
    template_name = "admin_panel_module/slider_list.html"
    paginate_by = 5
    context_object_name = "sliders"
    model = Slider

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        sliders_count = self.model.objects.all().count()
        context["slidersCount"] = sliders_count
        return context


class sliderDetail(View):
    def get(self, request: HttpRequest, pk):
        obj = Slider.objects.filter(pk=pk).first()
        form = SliderDetailsForm(instance=obj)
        return render(request, "admin_panel_module/slider_detail.html", {
            "form": form,
        })

    def post(self, request: HttpRequest, pk):
        obj = Slider.objects.filter(pk=pk).first()
        form = SliderDetailsForm(instance=obj, data=request.POST, files=request.FILES)
        is_active = request.POST.get("is_active")

        if form.is_valid():
            form.is_active = is_active
            # For refresh to remove cache to load image.
            form.save()
            return redirect(reverse_lazy('slider_detail', args=[obj.id]))

        return render(request, "admin_panel_module/slider_detail.html", {
            "form": form,
        })


class addSliderView(FormView):
    form_class = SliderDetailsForm
    template_name = "admin_panel_module/add_slider_page.html"
    success_url = "../slider/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class RemoveSliderView(View):
    def get(self, request):
        try:
            pk = request.GET.get("id")
            slider: Slider = get_object_or_404(Slider, pk=pk)
            slider.delete()
            return JsonResponse({
                "status": "ok",
            })

        except:
            return JsonResponse({
                "status": "error",
            })


def SetSliderEnableView(request):
    "Set slider active use for ajax and checkbox on slider list"
    try:
        id = request.GET.get("id")
        slider = get_object_or_404(Slider, pk=id)
        slider.is_active = True
        slider.save()
        return JsonResponse({
            "status": "ok"
        })

    except:
        return JsonResponse({
            "status": "error"
        })


def SetSliderDisableView(request):
    "Set slider active use for ajax and checkbox on slider list"
    try:
        id = request.GET.get("id")
        slider = get_object_or_404(Slider, pk=id)
        slider.is_active = False
        slider.save()
        return JsonResponse({
            "status": "ok"
        })

    except:
        return JsonResponse({
            "status": "error"
        })


class SiteSettingEditView(View):
    def get(self, request):
        site_setting = SiteSetting.objects.filter(is_active=True).first()
        form = SiteSettingsForm(instance=site_setting)
        return render(request, "admin_panel_module/site_settings_edit.html", {
            "form": form,
        })

    def post(self, request: HttpRequest):
        site_setting = SiteSetting.objects.filter(is_active=True).first()
        form = SiteSettingsForm(instance=site_setting, data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.is_active = True
            obj.save()
            messages.success(request, "اطلاعات سایت با موفقیت ویرایش شد!")

        return render(request, "admin_panel_module/site_settings_edit.html", {
            "form": form,
        })


class BannersListView(ListView):
    model = SiteBanners
    paginate_by = 5
    template_name = "admin_panel_module/banner_list.html"
    context_object_name = "banners"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        banners_count = SiteBanners.objects.all().count()
        context["bannersCount"] = banners_count

        # Remove messages (just to be sure)
        storage = messages.get_messages(self.request)
        list(storage)
        return context


class BannerEditPageView(View):
    def get(self, request: HttpRequest, pk):
        banner = get_object_or_404(SiteBanners, pk=pk)
        form = BannerEditForm(instance=banner)
        return render(request, "admin_panel_module/banner_edit.html", {
            "form": form,
        })

    def post(self, request: HttpRequest, pk):
        banner = get_object_or_404(SiteBanners, pk=pk)
        form = BannerEditForm(instance=banner, data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "تبلیغ شما با موفقیت ویرایش شد!")

        return render(request, "admin_panel_module/banner_edit.html", {
            "form": form,
        })


class AddBannerView(FormView):
    template_name = "admin_panel_module/add_banner.html"
    form_class = BannerEditForm
    success_url = reverse_lazy('banners_list_page')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "تبلیغ جدید افزوده شد.")
        return super().form_valid(form)
