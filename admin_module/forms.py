from django import forms

from site_module.models import SiteSetting


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
