from django import forms
from django.core.validators import MinLengthValidator


class loginForm(forms.Form):
    username = forms.CharField(max_length=100, error_messages={
        "required": "لطفا نام کاربری خود را وارد کنید!"
    }, widget=forms.TextInput(attrs={
        "placeholder": "نام کاربری"
    }), label="")

    password = forms.CharField(max_length=100, error_messages={
        "required": "لطفا نام کاربری خود را وارد کنید!"
    }, widget=forms.PasswordInput(attrs={
        "placeholder": "رمز عبور"
    }), label="")


class registerForm(forms.Form):
    username = forms.CharField(max_length=100, error_messages={
        "required": "لطفا نام کاربری خود را وارد کنید!"
    }, widget=forms.TextInput(attrs={
        "placeholder": "نام کاربری"
    }), label="", validators=[MinLengthValidator(4,
                                                 "حداقل تعداد کاراکتر های نام کاربری ۴ تا میباشد!")])

    email = forms.EmailField(max_length=100, error_messages={
        "required": "لطفا ایمیل خود را وارد کنید",
    }, widget=forms.EmailInput(attrs={
        "placeholder": "ایمیل"
    }), label="", validators=[MinLengthValidator(5,
                                                 "حداقل تعداد کاراکتر های ایمیل ۵ تا میباشد! ")])

    password = forms.CharField(max_length=100, error_messages={
        "required": "لطفا رمز عبور خود را وارد کنید!"
    }, widget=forms.PasswordInput(attrs={
        "placeholder": "رمز عبور"
    }), label="", validators=[MinLengthValidator(8,
                                                 "حداقل تعداد کاراکتر های رمز عبور ۸ تا میباشد! ")])

    confirm_password = forms.CharField(max_length=100, error_messages={
        "required": "لطفا تکرار رمز عبور خود را وارد کنید!"
    }, widget=forms.PasswordInput(attrs={
        "placeholder": "تکرار رمز عبور"
    }), label="", validators=[MinLengthValidator(8,
                                                 "حداقل تعداد کاراکتر های رمز عبور ۸ تا میباشد! ")])

    def clean(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("رمز عبور شما با تکرارش مطابقت ندارد! ")

        return self.cleaned_data
