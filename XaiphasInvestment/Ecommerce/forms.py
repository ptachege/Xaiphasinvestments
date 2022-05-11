from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.models import User
from .models import *

Payment_Choices = (
    ('Mpesa', 'Mpesa'),
    ('PayPal', 'Paypal'),
)


class AddStockForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'category', 'image','url']


class UserLogForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'Email'}),
        }
