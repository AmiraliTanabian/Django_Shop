from django import forms


class ProductCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "متن نظر"}
    ), label="")
