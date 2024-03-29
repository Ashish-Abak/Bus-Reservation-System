from django import forms
from django.contrib.auth.models import User

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    password = forms.CharField(widget=forms.PasswordInput)

    