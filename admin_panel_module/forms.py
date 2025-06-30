from django import forms

from news_module.models import Article
from site_module.models import Slider, SiteSetting


class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ["categories", "tags"]
        labels = {
            "title": "عنوان مقاله",
            "author": "نویسنده مقاله",
            "image": "تصویر اصلی مقاله",
            "short_info": "توضیحات کوتاه",
            "text": "متن مقاله",
            "data": "تاریخ ثبت مقاله",
            "is_active": "فعال / غیرفعال بودن مقاله"
        }


class SliderDetailsForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = Slider

        error_messages = {
            "title": {
                "required": "لطفا عنوان را وارد نمایید.",
                'max_length': "حداکثر طول فیلد عنوان ۵۰ کاراکتر است"
            },
            "banner": {
                "required": "لطفا تصویر اسلایدر را وارد نمایید.",
            },
            "text": {
                "required": "لطفا متن را وارد نمایید.",
                "max_length": "حداکثر طول فیلد متن اسلایدر ۲۵۵ کاراکتر است."
            },
            "url": {
                "required": "لطفا آدرس را وارد نمایید.",
            },
            "btn_text": {
                "required": "لطفا متن دکمه اسلایدر را وارد نمایید.",
                "max_length": "حداکثر طول متن دکمه اسلایدر ۲۵ کاراکتر است."
            },
        }


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = "__all__"

        error_messages = {
            "site_name": {"required": "لطفا نام سایت را وارد کنید.",
                          "max_length": "حداکثر کاراکتر مجاز برای نام سایت ۲۰۰ میباشد!!"},
            "site_url": {"required": "لطفا آدرس سایت را وارد کنید."},
            "address": {"required": "لطفا آدرس مجموعه را وارد کنید.",
                        "max_length": "حداکثر کاراکتر مجاز برای آدرس مجموعه ۲۵۵ میباشد!!"},
            "email": {"required": "لطفا ایمیل را وارد کنید.",
                      "max_length": "حداکثر کاراکتر مجاز برای ایمیل ۵۰ میباشد!!"},
            "phone": {"required": "لطفا نام سایت را وارد کنید.",
                      "max_length": "تلفن همراه نامعتبر است."},
            "fax": {"required": "لطفا فکس را وارد کنید.",
                    "max_length": "حداکثر کاراکتر مجاز برای فکس ۲۵۵ میباشد!!"},
            "copy_right": {"required": "لطفا متن کپی رایت را وارد کنید.",
                           "max_length": "حداکثر کاراکتر برای متن کپی رایت ۲۵۵ تا میباشد!!"},
            "about_us": {"required": "لطفا متن درباره ما را وارد کنید."},
            "site_logo": {"required": "لطفا لوگو سایت را وارد کنید."},
        }
