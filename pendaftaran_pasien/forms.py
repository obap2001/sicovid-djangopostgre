from django import forms
from django.db import connection

class CreatePasienForm(forms.Form):
    nik = forms.CharField(max_length=20,required=True)
    nama = forms.CharField(max_length=50, required=True)
    nomor_telepon = forms.CharField(max_length=20, required=True)
    nomor_hp = forms.CharField(max_length=12, required=True)

class CreatePasienKTPAlamatForm(forms.Form):
    jalan = forms.CharField(max_length=30, required=True)
    kelurahan = forms.CharField(max_length=30, required=True)
    kecamatan = forms.CharField(max_length=30, required=True)
    kabupaten_kota = forms.CharField(max_length=30, required=True)
    provinsi = forms.CharField(max_length=30, required=True)

class CreatePasienDomisiliAlamatForm(forms.Form):
    jalan = forms.CharField(max_length=30, required=True)
    kelurahan = forms.CharField(max_length=30, required=True)
    kecamatan = forms.CharField(max_length=30, required=True)
    kabupaten_kota = forms.CharField(max_length=30, required=True)
    provinsi = forms.CharField(max_length=30, required=True)





