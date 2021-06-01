from django import forms
from django.db import connection

def fetch_data_faskes():
    faskes_data_choice = []
    with connection.cursor() as cursor:
        cursor.execute(
        'SELECT Kode, Nama From siruco.FASKES;'
        )
        faskes_data_choice = cursor.fetchall()
    return tuple(faskes_data_choice)

class adminSistemRegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=20, required=True, widget=forms.PasswordInput())

class penggunaPublikRegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=20, required=True, widget=forms.PasswordInput())
    nama = forms.CharField(max_length=50, required=True)
    nik = forms.CharField(max_length=20, required=True)
    noHP = forms.CharField(max_length=12, required=True)

class adminDokterRegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=20, required=True, widget=forms.PasswordInput())
    noSTR = forms.CharField(max_length=20, required=True)
    nama = forms.CharField(max_length=50, required=True)
    noHP = forms.CharField(max_length=12, required=True)
    gelarDepan = forms.CharField(max_length=10, required=True)
    gelarBelakang = forms.CharField(max_length=10, required=True)

class adminSatgasRegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=20, required=True, widget=forms.PasswordInput())
    kode_faskes = forms.ChoiceField(choices=fetch_data_faskes())
