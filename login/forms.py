from django.core.exceptions import ValidationError
import re
from django import forms
from django.db import connection

class loginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=20, required=True, widget=forms.PasswordInput())

    def clean(self):
        form_data = self.cleaned_data
        form_password = form_data['password']
        check = re.search("([A-Z].*[0-9])|([0-9].*[A-Z])",form_password)
        if not check:
            raise ValidationError('Password harus minimal mengandung 1 huruf kapital dan 1 angka')




