from django import forms

class adminRegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=20, required=True)

class penggunaPublikRegisterForm(forms.Form):
    username = forms.CharField( max_length=50, required=True)
    password = forms.CharField(max_length=20, required=True)
    NIK = forms.CharField(max_length=20, required=True)
    nama = forms.CharField(max_length=50, required=True)
    status = forms.CharField(max_length=10, required=True)
    peran = forms.CharField(max_length=20, required=True)
    noHP = forms.CharField(max_length=12, required=True)

class adminSistemRegisterForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=20, required=True)
    peran = forms.CharField(max_length=20, required=True)

class adminDokterRegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=20, required=True)
    noSTR = forms.CharField(max_length=20, required=True)
    peran = forms.CharField(max_length=20, required=True)
    nama = forms.CharField(max_length=50, required=True)
    noHP = forms.CharField(max_length=12, required=True)
    gelarDepan = forms.CharField(max_length=10, required=True)
    gelarBelakang = forms.CharField(max_length=10, required=True)

class adminSatgasRegisterForm(forms.Form):gi
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=20, required=True)
    kode_faskes = forms.CharField(max_length=3, required=True)
