from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

from .models import ticket_model, PriorityChoices, UnitsChoices


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username", "email", "address", "phone_number", "about_user",
                  "profile_image"]
        labels = {
            "first_name": "", "last_name": "", "username": "", "email": "", "phone_number": "", "about_user": "",
            "profile_image": "عکس پروفایل", }

        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "نام",
                                                 "class": "form-control"
                                                 }),
            "last_name": forms.TextInput(attrs={"placeholder": "نام خانوادگی",
                                                "class": "form-control"
                                                }),
            "username": forms.TextInput(attrs={"placeholder": "نام کاربری",
                                               "class": "form-control"
                                               }),
            "email": forms.EmailInput(attrs={"placeholder": "ایمیل",
                                             "class": "form-control"
                                             }),
            "phone_number": forms.NumberInput(attrs={"placeholder": "تلفن همراه",
                                                     "class": "form-control"
                                                     }),
            "about_user": forms.Textarea(attrs={"placeholder": "درباره کاربر",
                                                "class": "form-control"
                                                }),
            "profile_image": forms.FileInput(attrs={"placeholder": "آواتار",
                                                    "class": "form-control",
                                                    "id": "fileInputOnProfile",
                                                    "hidden": "hidden",
                                                    }),
            "address": forms.Textarea(attrs={"placeholder": "آدرس",
                                             "class": "form-control"
                                             }),
        }


class EditPasswordForm(forms.Form):
    password = forms.CharField(label="",
                               widget=forms.PasswordInput(
                                   attrs={"placeholder": "رمز فعلی"
                                       , "title": "رمز عبور فعلی",
                                          'class': 'form-control'}),
                               error_messages={"required": "رمز عبور فعلی خود را وارد نکردید!"})

    new_password = forms.CharField(label="",
                                   widget=forms.PasswordInput(
                                       attrs={"placeholder": "رمز جدید"
                                           , "title": "رمز عبور جدید",
                                              'class': 'form-control'}),
                                   error_messages={"required": "رمز عبور جدید خود را وارد نکردید!"},
                                   validators=
                                   [MinLengthValidator(8, "حداقل تعداد کاراکتر های رمز عبور ۸ تا می باشد:)")]
                                   )

    new_password_confirm = forms.CharField(label="",
                                           widget=forms.PasswordInput(
                                               attrs={"placeholder": " تکرار رمز جدید"
                                                   , "title": "تکرار رمز عبور جدید",
                                                      'class': 'form-control'}),
                                           error_messages={"required": "تکرار رمز عبور جدید خود را وارد نکردید!"})

    def clean(self):
        if "new_password" in self.cleaned_data:
            new_password = self.cleaned_data["new_password"]
            new_password_confirm = self.cleaned_data["new_password_confirm"]

            if new_password != new_password_confirm:
                raise forms.ValidationError("رمز شما با تکرارش مطابقت ندارد!")

        return self.cleaned_data


class AddTicketModelForm(forms.ModelForm):
    class Meta:
        model = ticket_model
        fields = ["title", "Priority", "Unit", "text", "user"]

        widgets = {
            "text": forms.widgets.Textarea(attrs={"class": "form-control"}),
            "title": forms.widgets.TextInput(attrs={"class": "form-control"}),
            "Priority": forms.widgets.Select(attrs={"class": "form-control"}),
            "Unit": forms.widgets.Select(attrs={"class": "form-control"}),
            "user": forms.widgets.HiddenInput()
        }


class AddTicketForm(forms.Form):
    title = forms.CharField(widget=forms.widgets.TextInput(attrs={"class": "form-control"}), label="عنوان")
    priority = forms.CharField(widget=forms.widgets.Select(attrs={"class": "form-control"}, choices=PriorityChoices),
                               label="اولویت")
    unit = forms.CharField(widget=forms.widgets.Select(attrs={"class": "form-control"}, choices=UnitsChoices),
                           label="واحد مربوطه")
    text = forms.CharField(widget=forms.widgets.Textarea(attrs={"class": "form-control"}), label="متن")
