from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].required = False

    class Meta:
        model = User
        fields = ('avatar', 'user_name', 'email', 'first_name', 'last_name', 'password')


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar', 'user_name', 'email', 'first_name', 'last_name', 'about')
