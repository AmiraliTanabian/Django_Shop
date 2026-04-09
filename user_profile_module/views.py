from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from phonenumbers import parse, is_valid_number

from order_module.models import orderModel
from .forms import EditProfileModelForm, EditPasswordForm, AddTicketForm, TicketAnswerForm
from .models import ticket_model, TicketAnswerModel, ticket_attachment


class ProfileDashboardPage(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login_page")
    template_name = "user_profile_module/user_dashboard_page.html"


class EditProfilePageView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login_page")

    def get(self, request: HttpRequest):
        edit_profile_form = EditProfileModelForm(instance=request.user)
        return render(request, "user_profile_module/edit_profile_page.html",
                      {"form": edit_profile_form})

    def post(self, request: HttpRequest):
        edit_profile_form = EditProfileModelForm(request.POST, request.FILES, instance=request.user)

        if edit_profile_form.is_valid():
            mobile = edit_profile_form.cleaned_data["phone_number"]
            email = edit_profile_form.cleaned_data["email"].strip()

            # mobile validation
            if mobile is not None:
                try:
                    parsed_number = parse(mobile, "IR")
                    mobile_validation = is_valid_number(parsed_number)
                except:
                    mobile_validation = False

                # Second step for mobile validation
                mobile_exists = get_user_model().objects.filter(phone_number=mobile)
                if mobile_exists and mobile_exists == request.user:
                    mobile_validation = False

            # dont have mobile
            else:
                messages.error(request, "فیلد موبایل ضرروری مبیاشد")
                return render(request, "user_profile_module/edit_profile_page.html",
                              {"form": edit_profile_form})

            # email validation
            if email != '':
                email_exists = get_user_model().objects.filter(email=email).first()
                if email_exists and email_exists != request.user:
                    email_validation = False
                else:
                    email_validation = True

            # dont have email
            else:
                messages.error(request, "فیلد ایمیل ضرروری مبیاشد")
                return render(request, "user_profile_module/edit_profile_page.html",
                              {"form": edit_profile_form})

            if email_validation and mobile_validation:
                edit_profile_form.save()
                messages.success(request, "اطلاعات شما ویرایش شد")
                return render(request, "user_profile_module/edit_profile_page.html",
                              {"form": edit_profile_form})

            elif not email_validation:
                messages.error(request, "این ایمیل قبلا ثبت شده :(")
                return render(request, "user_profile_module/edit_profile_page.html",
                              {"form": edit_profile_form})

            # invalid phone number
            else:
                messages.error(request, "متاسفانه موبایل شما نادرست است :(")
                return render(request, "user_profile_module/edit_profile_page.html",
                              {"form": edit_profile_form})

        # form is invalid
        else:
            return render(request, "user_profile_module/edit_profile_page.html",
                          {"form": edit_profile_form})


class EditPasswordPageView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login_page")

    def get(self, request):
        form = EditPasswordForm
        return render(request, "user_profile_module/edit_password_page.html", {"form": form})

    def post(self, request):
        form = EditPasswordForm(request.POST)

        if form.is_valid():
            user = get_user_model().objects.get(id=request.user.id)
            old_password = form.cleaned_data.get("password")
            new_password = form.cleaned_data.get("new_password")
            is_password_correct = check_password(old_password, user.password)

            if is_password_correct:
                user.set_password(new_password)
                user.save()
                messages.success(request, "رمز عبور شما با موفقیت تغییر کرد")
                return render(request, "user_profile_module/edit_password_page.html", {"form": form})

            else:
                messages.error(request, "رمز عبور شما با نادرست است.")
                return render(request, "user_profile_module/edit_password_page.html", {"form": form})

        else:
            return render(request, "user_profile_module/edit_password_page.html", {"form": form})


class ProfileFavoriteProductsView(LoginRequiredMixin, ListView):
    template_name = "user_profile_module/favorite_list_on_profile.html"
    context_object_name = "products"
    login_url = reverse_lazy("login_page")
    model = get_user_model()
    paginate_by = 5

    def get_queryset(self):
        user_id = self.request.user.id
        query = get_user_model().objects.get(id=user_id)
        query = query.favorite_products.all()
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        favorite_products = user.favorite_products.all()
        context["favorite_list"] = favorite_products
        return context


class ProfileOrders(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("login_page")
    template_name = "user_profile_module/user_orders_list.html"
    model = orderModel
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        query = orderModel.objects.filter(is_paid=True, user=self.request.user)
        return query


class orderPageView(LoginRequiredMixin, DetailView):
    template_name = "user_profile_module/order_detail.html"
    context_object_name = "order"
    model = orderModel

    def get_queryset(self):
        query = super().get_queryset()
        query.filter(user=self.request.user).prefetch_related("orderproductmodel_set")
        return query


class AddTickerView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login_page")

    def get(self, request: HttpRequest):
        form = AddTicketForm()
        return render(request, "user_profile_module/add_ticket.html", {
            "form": form
        })

    def post(self, request: HttpRequest):
        form = AddTicketForm(request.POST, request.FILES)
        if form.is_valid():
            current_ticket = ticket_model(title=form.cleaned_data.get("title"),
                                          user=request.user,
                                          Priority=form.cleaned_data.get("priority"),
                                          Unit=form.cleaned_data.get("unit"),
                                          text=form.cleaned_data.get("text"))
            current_ticket.save()

            # Ticket attachment part:
            ticket_attachments = request.POST.get("files_id_list").split(",")
            ticket_attachments.remove("")
            for id in ticket_attachments:
                attachment = ticket_attachment.objects.get(id=int(id))
                attachment.ticket = current_ticket
                attachment.save()

            messages.success(request, "تیکت شما با موفقیت ثبت شد \n پاسخ آن را در همان بخش دریافت میکنید")
            return redirect(reverse_lazy("ticket_list_page"))

        return render(request, "user_profile_module/add_ticket.html", {
            "form": form
        })


class TicketList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("login_page")
    model = ticket_model
    paginate_by = 5
    template_name = "user_profile_module/ticket_list.html"
    context_object_name = "tickets"

    def get_queryset(self):
        query = ticket_model.objects.filter(is_active=True, user=self.request.user)
        return query


class TicketDetailView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login_page")

    def get(self, request: HttpRequest, id):
        current_ticket = ticket_model.objects.filter(id=int(id), user=self.request.user, is_active=True).first()
        reply_form = TicketAnswerForm()
        answers = TicketAnswerModel.objects.filter(ticket=current_ticket)
        return render(request, "user_profile_module/ticket_detail.html", {
            "ticket": current_ticket,
            "reply_form": reply_form,
            "answers": answers,
        })

    def post(self, request: HttpRequest, id):
        current_ticket = ticket_model.objects.filter(id=int(id), user=self.request.user, is_active=True).first()
        reply_form = TicketAnswerForm(request.POST)
        answers = TicketAnswerModel.objects.filter(ticket=current_ticket).order_by("-id")

        if reply_form.is_valid():
            TicketAnswerModel.objects.create(text=reply_form.cleaned_data.get("text"),
                                             user=request.user,
                                             ticket=current_ticket
                                             )
            return redirect(reverse_lazy("ticket_detail_page", args=[id]))

        return render(request, "user_profile_module/ticket_detail.html", {
            "ticket": current_ticket,
            "reply_form": reply_form,
            "answers": answers,

        })


@login_required
def ticket_add_file_ajax(request):
    if request.method == "POST":
        file = request.FILES.get('ticket_file')

        if file:
            attachment = ticket_attachment.objects.create(files=file)

            return JsonResponse({
                'success': True,
                "msg": "file added!",
                'file_id': attachment.id
            })
        else:
            return JsonResponse({'success': False, 'error': 'فایلی دریافت نشد'}, status=400)

    return JsonResponse({'success': False, 'error': 'درخواست نامعتبر'}, status=400)


@login_required
def remove_ticket_file(request, id):
    if request.method == "GET":
        file = get_object_or_404(ticket_attachment, id=int(id))
        file.delete()

        return JsonResponse({
            'success': True,
            "msg": "file removed!",
            'file_id': id
        })
