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
from product_module.models import Product, Brand, ProductTag, ProductComment
from site_module.models import Slider, SiteSetting, SiteBanners
from .forms import (ArticleEditForm, SliderDetailsForm, SiteSettingsForm, BannerEditForm, ProductEditForm,
                    BrandEditForm, ProductTagEditForm)


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


class RemoveBannerView(View):
    def get(self, request: HttpRequest):
        try:
            pk = request.GET.get("id")
            banner: SiteBanners = get_object_or_404(SiteBanners, pk=pk)
            banner.delete()
            return JsonResponse({
                "status": "ok",
            })

        except:
            return JsonResponse({
                "status": "error",
            })


class ProductListView(ListView):
    template_name = "admin_panel_module/product_list.html"
    paginate_by = 6
    context_object_name = "products"
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["productCount"] = Product.objects.all().count()
        return context


class RemoveProductViewAjax(View):
    def get(self, request: HttpRequest):
        try:
            pk = request.GET.get("id")
            product: Product = get_object_or_404(Product, pk=pk)
            product.delete()
            return JsonResponse({
                "status": "ok",
            })

        except:
            return JsonResponse({
                "status": "error",
            })


def change_product_count_ajax(request: HttpRequest):
    product_id = request.GET.get("id")
    count = request.GET.get("count")
    product = get_object_or_404(Product, pk=int(product_id))
    product.count = int(count)
    product.save()
    return JsonResponse({
        "status": "ok",
    })


class ProductDetailView(View):
    def get(self, request: HttpRequest, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductEditForm(instance=product)
        return render(request, "admin_panel_module/product_detail.html", {
            "form": form,
        })

    def post(self, request: HttpRequest, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductEditForm(instance=product, files=request.FILES, data=request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.is_available = True
            form_obj.save()
            messages.success(request, "محصول مورد نظر ویرایش شد!")

        return render(request, "admin_panel_module/product_detail.html", {
            "form": form,
        })


class BrandListView(ListView):
    paginate_by = 6
    template_name = "admin_panel_module/brand_list.html"
    model = Brand
    context_object_name = "brands"
    ordering = ["-id"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["BrandCount"] = Brand.objects.all().count()
        return context


def SetBrandEnableView(request):
    "Set brand enable use for ajax and checkbox on slider list"
    try:
        id = request.GET.get("id")
        brand = get_object_or_404(Brand, pk=id)
        brand.is_active = True
        brand.save()
        return JsonResponse({
            "status": "ok"
        })

    except:
        return JsonResponse({
            "status": "error"
        })


def SetBrandDisableView(request):
    "Set brand disable use for ajax and checkbox on slider list"
    try:
        id = request.GET.get("id")
        brand = get_object_or_404(Brand, pk=id)
        brand.is_active = False
        brand.save()
        return JsonResponse({
            "status": "ok"
        })

    except:
        return JsonResponse({
            "status": "error"
        })


class AddBrandPageView(FormView):
    form_class = BrandEditForm
    template_name = "admin_panel_module/add_brand_page.html"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "برند با موفقیت ارسال شد.")
        return redirect(reverse_lazy('brand_list_page'))

    def form_invalid(self, form):
        return render(self.request, "admin_panel_module/add_brand_page.html", {
            "form": form,
        })


class RemoveBrandAjax(View):
    def get(self, request: HttpRequest):
        try:
            pk = request.GET.get("id")
            brand: Brand = get_object_or_404(Brand, pk=pk)
            brand.delete()
            return JsonResponse({
                "status": "ok",
            })

        except:
            return JsonResponse({
                "status": "error",
            })


class BrandEditPageView(View):
    def get(self, request: HttpRequest, pk):
        brand = get_object_or_404(Brand, pk=pk)
        form = BrandEditForm(instance=brand)
        return render(request, "admin_panel_module/edit_brand.html", {
            "form": form,
        })

    def post(self, request: HttpRequest, pk):
        brand = get_object_or_404(Brand, pk=pk)
        form = BrandEditForm(instance=brand, data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "برند شما با موفقیت ویرایش شد!")

        return render(request, "admin_panel_module/edit_brand.html", {
            "form": form,
        })


class ProductBrandList(ListView):
    template_name = "admin_panel_module/product_tags_list.html"
    paginate_by = 6
    ordering = ['-id']
    model = ProductTag
    context_object_name = "tags"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["productTagCount"] = ProductTag.objects.all().count()
        return context


def SetProductTagEnableView(request):
    "Set Product tag enable use for ajax and checkbox on slider list"
    try:
        id = request.GET.get("id")
        product_tag = get_object_or_404(ProductTag, pk=id)
        product_tag.is_active = True
        product_tag.save()
        return JsonResponse({
            "status": "ok"
        })

    except:
        return JsonResponse({
            "status": "error"
        })


def SetProductTagDisableView(request):
    "Set Product tag disable use for ajax and checkbox on slider list"
    try:
        id = request.GET.get("id")
        product_tag = get_object_or_404(ProductTag, pk=id)
        product_tag.is_active = False
        product_tag.save()
        return JsonResponse({
            "status": "ok"
        })

    except:
        return JsonResponse({
            "status": "error"
        })


class RemoveProductTagAjax(View):
    def get(self, request: HttpRequest):
        try:
            pk = request.GET.get("id")
            product_tag: ProductTag = get_object_or_404(ProductTag, pk=int(pk))
            product_tag.delete()
            return JsonResponse({
                "status": "ok",
            })

        except:
            return JsonResponse({
                "status": "error",
            })


class ProductTagEditPageView(View):
    def get(self, request: HttpRequest, pk):
        product_tag = get_object_or_404(ProductTag, pk=pk)
        form = ProductTagEditForm(instance=product_tag)
        return render(request, "admin_panel_module/product_tag_edit.html", {
            "form": form,
        })

    def post(self, request: HttpRequest, pk):
        product_tag = get_object_or_404(ProductTag, pk=pk)
        form = ProductTagEditForm(instance=product_tag, data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "تگ شما با موفقیت ویرایش شد!")

        return render(request, "admin_panel_module/product_tag_edit.html", {
            "form": form,
        })


class AddProductTagPageView(FormView):
    form_class = ProductTagEditForm
    template_name = "admin_panel_module/add_product_tag.html"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "نگ شما با موفقیت افزوده شد")
        return redirect(reverse_lazy('product_tag_list_page'))

    def form_invalid(self, form):
        return render(self.request, "admin_panel_module/add_product_tag.html", {
            "form": form,
        })


class ProductCommentsList(ListView):
    template_name = "admin_panel_module/product_comments_list.html"
    context_object_name = "comments"
    ordering = ["-id"]
    model = ProductComment
    paginate_by = 8

    def get_queryset(self):
        # productcomment_set : comment replies
        query = ProductComment.objects.filter(parent=None).prefetch_related('productcomment_set').all()
        self.count = query.count()
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['commentCount'] = self.count
        return context


def set_product_comment_approved(request:HttpRequest):
    comment_id = request.GET.get("id")
    comment = get_object_or_404(ProductComment, id=comment_id)
    if comment.status == "approved":
        return JsonResponse({
            "status":"error",
            "msg":"The comment for the selected product has already been approved; you cannot activate it again"
        })

    else:
        comment.status = "approved"
        comment.save()
        return JsonResponse({
            "status":"ok",
        })

def set_product_comment_rejected(request:HttpRequest):
    comment_id = request.GET.get("id")
    comment = get_object_or_404(ProductComment, id=comment_id)
    if comment.status == "rejected":
        return JsonResponse({
            "status":"error",
            "msg":"The comment for the selected product has already been rejected; you cannot activate it again"
        })

    else:
        comment.status = "rejected"
        comment.save()
        return JsonResponse({
            "status":"ok",
        })