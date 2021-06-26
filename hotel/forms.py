from django import forms
from django.db import connection

class CreateHotelForm(forms.Form):
    kode = forms.CharField(max_length=5, disabled=True)
    namaHotel = forms.CharField(max_length=30, required=True)
    rujukan = forms.BooleanField(required=False)

class CreateAlamatHotelForm(forms.Form):
    jalan = forms.CharField(label='Jalan' ,max_length=30, required=True)
    kelurahan = forms.CharField(label='Kelurahan/Desa', max_length=30, required=True)
    kecamatan = forms.CharField(label='Kecamatan',max_length=30, required=True)
    kabupaten_kota = forms.CharField(label='Kabupaten/Kota',max_length=30, required=True)
    provinsi = forms.CharField(label='Provinsi', max_length=30, required=True) 

class FormUpdateHotel(forms.Form):
    kode = forms.CharField(max_length=5, disabled=True)
    nama = forms.CharField(max_length=30, required=True)
    rujukan = forms.BooleanField(required=False)

class FormUpdateAlamatHotel(forms.Form):
    jalan = forms.CharField(label='Jalan' ,max_length=30, required=True)
    kelurahan = forms.CharField(label='Kelurahan/Desa', max_length=30, required=True)
    kecamatan = forms.CharField(label='Kecamatan',max_length=30, required=True)
    kabupaten_kota = forms.CharField(label='Kabupaten/Kota',max_length=30, required=True)
    provinsi = forms.CharField(label='Provinsi', max_length=30, required=True)