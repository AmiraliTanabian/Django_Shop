from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from contact_module.models import ContactModel
from news_module.models import Article
from site_module.models import SiteSetting, SiteBanners, Slider


class SettingEditForms(forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = "__all__"

        widgets = {
            "site_name": forms.widgets.TextInput(
                attrs={
                    "class": "form-control input-xs",
                    "placeholder": "متن سایت",
                    "id": "xsinput",

                }),
            "site_url": forms.widgets.URLInput(
                attrs={
                    "class": "form-control input-xs",
                    "placeholder": "آدرس سایت",
                    "id": "xsinput",

                }),
            "address": forms.widgets.Textarea(
                attrs={
                    "class": "form-control input-xs",
                    "placeholder": "آدرس",
                    "id": "xsinput",

                }),
            "email": forms.widgets.EmailInput(
                attrs={
                    "class": "form-control input-xs",
                    "placeholder": "ایمیل",
                    "id": "xsinput",

                }),
            "phone": forms.widgets.TextInput(
                attrs={
                    "class": "form-control input-xs",
                    "placeholder": "تلفن همراه",
                    "id": "xsinput",

                }),
            "fax": forms.widgets.TextInput(
                attrs={
                    "class": "form-control input-xs",
                    "placeholder": "فکس",
                    "id": "xsinput",

                }),
            "copy_right": forms.widgets.Textarea(
                attrs={
                    "class": "form-control input-xs",
                    "placeholder": "متن کپی رایت",
                    "id": "xsinput",

                }),
            "about_us": forms.widgets.Textarea(
                attrs={
                    "class": "form-control input-xs",
                    "placeholder": "متن درباره ما",
                    "id": "xsinput",

                }),
            "site_logo": forms.widgets.FileInput(
                attrs={
                    "class": "form-control input-xs",
                    "id": "xsinput",

                }),
            "is_active": forms.widgets.CheckboxInput(
                attrs={
                    "class": "form-control input-xs",
                    "id": "xsinput",

                }),
        }


class BannersEditForm(forms.ModelForm):
    class Meta:
        model = SiteBanners
        fields = "__all__"


class EditSliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = '__all__'


class AdminContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = "__all__"

        widgets = {
            "msg": forms.Textarea(
                attrs={
                    "class": "form-control input-xs",
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control input-xs",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control input-xs",
                }
            ),

            "subject": forms.TextInput(
                attrs={
                    "class": "form-control input-xs",
                }
            ),

            "answer": forms.Textarea(
                attrs={
                    "class": "form-control input-xs",
                }
            ),

        }


class EditArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ("author", "data")

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control input-xs",
                }
            ),

            "short_info": forms.TextInput(
                attrs={
                    "class": "form-control input-xs",
                }
            ),
            "text": CKEditor5Widget(
                attrs={
                    "class": "django_ckeditor_5 form-control input-xs",
                }
            ),

        }
