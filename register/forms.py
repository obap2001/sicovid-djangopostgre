from django.core.exceptions import ValidationError
import re
from django import forms
from django.db import connection

def fetch_data_faskes():
    faskes_data_choice = []
    with connection.cursor() as cursor:
        cursor.execute(
        'SELECT Kode, Nama From siruco.FASKES;'
        )
        faskes_data_choice = cursor.fetchall() #Will Get all output of the query
    return tuple(faskes_data_choice)

class adminSistemRegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=20, required=True, widget=forms.PasswordInput())
    def clean(self):
        form_data = self.cleaned_data
        if not re.search("([A-Z].*[0-9])|([0-9].*[A-Z])",form_data['password']):
            raise ValidationError('Password harus minimal mengandung 1 huruf kapital dan 1 angka')

class penggunaPublikRegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=20, required=True, widget=forms.PasswordInput())
    nama = forms.CharField(max_length=50, required=True)
    nik = forms.CharField(max_length=20, required=True)
    noHP = forms.CharField(max_length=12, required=True)
    def clean(self):
        form_data = self.cleaned_data
        if re.search("([A-Z].*[0-9])|([0-9].*[A-Z])",form_data['password']):
            raise ValidationError('Password harus minimal mengandung 1 huruf kapital dan 1 angka')

        if not re.search("([A-Z].*[0-9])|([0-9].*[A-Z])",form_data['password']):
            raise ValidationError('Password harus minimal mengandung 1 huruf kapital dan 1 angka')

class adminDokterRegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=20, required=True, widget=forms.PasswordInput())
    noSTR = forms.CharField(max_length=20, required=True)
    nama = forms.CharField(max_length=50, required=True)
    noHP = forms.CharField(max_length=12, required=True)
    gelarDepan = forms.CharField(max_length=10, required=True)
    gelarBelakang = forms.CharField(max_length=10, required=True)
    def clean(self):
        form_data = self.cleaned_data
        if not re.search("([A-Z].*[0-9])|([0-9].*[A-Z])",form_data['password']):
            raise ValidationError('Password harus minimal mengandung 1 huruf kapital dan 1 angka')

class adminSatgasRegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=20, required=True, widget=forms.PasswordInput())
    kode_faskes = forms.ChoiceField(choices=fetch_data_faskes())
    def clean(self):
        form_data = self.cleaned_data
        if not re.search("([A-Z].*[0-9])|([0-9].*[A-Z])",form_data['password']):
            raise ValidationError('Password harus minimal mengandung 1 huruf kapital dan 1 angka')

