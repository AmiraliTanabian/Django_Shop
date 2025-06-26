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
