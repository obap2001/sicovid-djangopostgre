from django import forms
from django.db import connection

class loginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=20, required=True, widget=forms.PasswordInput())




