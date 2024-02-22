from django.contrib.auth import get_user_model
from django import forms


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].required = False

    class Meta:
        model = get_user_model()
        fields = ('avatar', 'user_name', 'email', 'first_name', 'last_name', 'password')


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].required = False

    class Meta:
        model = get_user_model()
        fields = ('avatar', 'user_name', 'email', 'first_name', 'last_name', 'about')
