from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from auth_module.models import User
from contact_module.models import ContactModel
from news_module.models import Article, ArticleCategories, ArticleTag, ArticleComment
from order_module.models import orderModel
from product_module.models import Product, ProductCategory, ProductTag, ProductComment, Brand
from site_module.models import SiteSetting, SiteBanners, Slider
from user_profile_module.models import TicketAnswerModel, ticket_model


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


class AddArticleCatForm(forms.ModelForm):
    class Meta:
        model = ArticleCategories
        fields = "__all__"

        widgets = {
            "slug": forms.TextInput(
                attrs={
                    "class": "form-control input-xs",
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "form-control input-xs",
                }
            ),
        }


class AddArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = "__all__"

        widgets = {
            "slug": forms.TextInput(
                attrs={
                    "class": "form-control input-xs",
                }
            ),

            "tag_name": forms.TextInput(
                attrs={
                    "class": "form-control input-xs",
                }
            ),
        }


class EditCommentForms(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ("status",)


class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ("is_available", "order_count")

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control input-xs",
            }),
            "price": forms.TextInput(attrs={
                "class": "form-control input-xs",
            }),
            "count": forms.TextInput(attrs={
                "class": "form-control input-xs",
            }),
            "info": CKEditor5Widget(attrs={
                "class": "django_ckeditor_5 form-control input-xs",
            }),
        }


class AddProductCatForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = "__all__"

        widgets = {
            "slug": forms.TextInput(
                attrs={
                    "class": "form-control input-xs",
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "form-control input-xs",
                }
            ),
        }


class AddProductTagForm(forms.ModelForm):
    class Meta:
        model = ProductTag
        fields = "__all__"

        widgets = {
            "slug": forms.TextInput(
                attrs={
                    "class": "form-control input-xs",
                }
            ),

            "tag_name": forms.TextInput(
                attrs={
                    "class": "form-control input-xs",
                }
            ),
        }


class EditProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ("status",)


class AddProductBrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = "__all__"

        widgets = {
            "slug": forms.TextInput(
                attrs={
                    "class": "form-control input-xs",
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "form-control input-xs",
                }
            ),
        }


class EditOrder(forms.ModelForm):
    class Meta:
        model = orderModel
        fields = ("status",)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "address", "about_user", "profile_image",
                  "phone_number")

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control input-xs",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control input-xs",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control input-xs",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control input-xs",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control input-xs",
                }
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-control input-xs",
                }
            ),
            "about_user": forms.Textarea(
                attrs={
                    "class": "form-control input-xs",
                }
            ),
        }


class SendTicketReplyForm(forms.ModelForm):
    class Meta:
        model = TicketAnswerModel
        fields = ("text",)

        widgets = {"text": CKEditor5Widget(
            attrs={
                "class": "django_ckeditor_5 form-control input-xs",
                "placeholder": "متن پاسخ خود را اینجا قرار بدید."
            }
        ),
        }


class TicketUnitUpdateForm(forms.ModelForm):
    class Meta:
        model = ticket_model
        fields = ("Unit",)
        widgets = {
            "Unit": forms.Select(attrs={
                "class": "select-chip",
                "aria-label": "واحد مربوطه",
            })
        }
