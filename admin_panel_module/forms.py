from django import forms

from news_module.models import Article
from site_module.models import Slider


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
