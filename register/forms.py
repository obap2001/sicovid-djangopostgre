from django import forms

class adminRegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=20, required=True)

class penggunaPublikRegisterForm(forms.Form):
    username = forms.CharField( max_length=50, required=True)
    NIK = forms.CharField(max_length=20, required=True)
    nama = forms.CharField(max_length=50, required=True)
    status = forms.CharField(max_length=10, required=True)
    peran = forms.CharField(max_length=20, required=True)
    noHP = forms.CharField(max_length=12, required=True)