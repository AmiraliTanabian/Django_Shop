import re

from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView

from contact_module.models import ContactModel
from news_module.models import Article
from .forms import ArticleEditForm


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
        # Set msg to unread
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
