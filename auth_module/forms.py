from django import forms

class loginForm(forms.Form):
    username = forms.CharField(max_length=100, error_messages={
        "required":"لطفا نام کاربری خود را وارد کنید!"
    }, widget=forms.TextInput(attrs={
        "placeholder":"نام کاربری"
    }), label="")

    password = forms.CharField(max_length=100, error_messages={
        "required":"لطفا نام کاربری خود را وارد کنید!"
    }, widget=forms.PasswordInput(attrs={
        "placeholder":"رمز عبور"
    }), label="")