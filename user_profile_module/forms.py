from django import forms
from django.contrib.auth import get_user_model


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username", "email", "address", "phone_number", "about_user",
                  "profile_image"]
        labels = {
            "first_name" : "", "last_name" : "", "username":"", "email":"", "phone_number":"", "about_user":"",
            "profile_image":"عکس آواتار", }

        widgets = {
            "first_name" : forms.TextInput(attrs={"placeholder":"نام",
                                                  "class":"form-control"
                                                  }),
            "last_name" : forms.TextInput(attrs={"placeholder":"نام خانوادگی",
                                                 "class":"form-control"
                                                 }),
            "username" : forms.TextInput(attrs={"placeholder":"نام کاربری",
                                                "class":"form-control"
                                                }),
            "email" :  forms.EmailInput(attrs={"placeholder":"ایمیل",
                                               "class":"form-control"
                                               }),
            "phone_number" :  forms.NumberInput(attrs={"placeholder":"تلفن همراه",
                                                       "class":"form-control"
                                                       }),
            "about_user" : forms.Textarea(attrs={"placeholder":"درباره کاربر",
                                                 "class":"form-control"
                                                 }),
            "profile_image" : forms.FileInput(attrs={"placeholder":"آواتار",
                                                     "class":"form-control",
                                                     "id":"fileInputOnProfile",
                                                     "hidden":"hidden",
                                                     }),
            "address" : forms.Textarea(attrs={"placeholder":"آدرس",
                                              "class":"form-control"
                                              }),
        }