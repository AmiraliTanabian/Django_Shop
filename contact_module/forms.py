from django import forms
from .models import ContactModel

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        exclude = ["is_read"]

        error_messages = {
            "subject" : {"required" : "وارد کردن موضوع ضروری می باشد!"},
            "email" : {"required": "وارد کردن ایمیل ضروری میباشد!"},
            "name" : {"required":"وارد کردن نام ضروری مبباشد!"},
            "msg" : {"required":"وارد کردن پیام ضروری مبباشد "},
        }

        widgets = {
            "subject" : forms.TextInput(attrs={"placeholder" : "موضوع",
                                               "class":"form-control"} ),
            "email" : forms.EmailInput(attrs={"placeholder": "ایمیل",
                                              "class":"form-control"} ),
            "name" : forms.TextInput(attrs={"placeholder":"نام",
                                            "class":"form-control"} ),
            "msg" : forms.Textarea(attrs={"placeholder":"پیام ",
                                          "class":"form-control", "id":"message"} )
        }

        labels = {
            "subject":"",
            "email":"",
            "name":"",
            "msg":"",
        }