from django import forms
from django.db import connection

class CreatePasienForm(forms.Form):
    pendaftar = forms.CharField(max_length=50, disabled=True)
    nik = forms.CharField(label='NIK',max_length=20,required=True)
    nama = forms.CharField(max_length=50, required=True)
    nomor_telepon = forms.CharField(max_length=20, required=True)
    nomor_hp = forms.CharField(max_length=12, required=True)

class CreatePasienKTPAlamatForm(forms.Form):
    jalan = forms.CharField(max_length=30, required=True)
    kelurahan = forms.CharField(max_length=30, required=True)
    kecamatan = forms.CharField(max_length=30, required=True)
    kabupaten_kota = forms.CharField(label='Kabupaten/Kota',max_length=30, required=True)
    provinsi = forms.CharField(max_length=30, required=True)

class CreatePasienDomisiliAlamatForm(forms.Form):
    jalan = forms.CharField(max_length=30, required=True)
    kelurahan = forms.CharField(max_length=30, required=True)
    kecamatan = forms.CharField(max_length=30, required=True)
    kabupaten_kota = forms.CharField(label='Kabupaten/Kota',max_length=30, required=True)
    provinsi = forms.CharField(max_length=30, required=True)

class DetailPasienForm(forms.Form):
    pendaftar = forms.CharField(max_length=50, disabled=True)
    nik = forms.CharField(label='NIK',max_length=20,required=True, disabled=True)
    nama = forms.CharField(max_length=50, required=True, disabled=True)
    nomor_telepon = forms.CharField(max_length=20, required=True, disabled=True)
    nomor_hp = forms.CharField(max_length=12, required=True, disabled=True)

class DetailPasienKTPAlamatForm(forms.Form):
    jalan = forms.CharField(max_length=30, required=True, disabled=True)
    kelurahan = forms.CharField(max_length=30, required=True, disabled=True)
    kecamatan = forms.CharField(max_length=30, required=True, disabled=True)
    kabupaten_kota = forms.CharField(label='Kabupaten/Kota',max_length=30, required=True, disabled=True)
    provinsi = forms.CharField(max_length=30, required=True, disabled=True)

class DetailPasienDomisiliAlamatForm(forms.Form):
    jalan = forms.CharField(max_length=30, required=True, disabled=True)
    kelurahan = forms.CharField(max_length=30, required=True, disabled=True)
    kecamatan = forms.CharField(max_length=30, required=True, disabled=True)
    kabupaten_kota = forms.CharField(label='Kabupaten/Kota',max_length=30, required=True, disabled=True)
    provinsi = forms.CharField(max_length=30, required=True, disabled=True)


class UpdatePasienForm(forms.Form):
    pendaftar = forms.CharField(max_length=50, disabled=True)
    nik = forms.CharField(label='NIK',max_length=20,required=True, disabled=True)
    nama = forms.CharField(max_length=50, required=True, disabled=True)
    nomor_telepon = forms.CharField(max_length=20, required=True)
    nomor_hp = forms.CharField(max_length=12, required=True)

class UpdatePasienKTPAlamatForm(forms.Form):
    jalan = forms.CharField(max_length=30, required=True)
    kelurahan = forms.CharField(max_length=30, required=True)
    kecamatan = forms.CharField(max_length=30, required=True)
    kabupaten_kota = forms.CharField(label='Kabupaten/Kota',max_length=30, required=True)
    provinsi = forms.CharField(max_length=30, required=True)

class UpdatePasienDomisiliAlamatForm(forms.Form):
    jalan = forms.CharField(max_length=30, required=True)
    kelurahan = forms.CharField(max_length=30, required=True)
    kecamatan = forms.CharField(max_length=30, required=True)
    kabupaten_kota = forms.CharField(label='Kabupaten/Kota',max_length=30, required=True)
    provinsi = forms.CharField(max_length=30, required=True)






