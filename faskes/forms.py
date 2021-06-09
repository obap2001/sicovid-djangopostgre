from django import forms
from django.db import connection

tipe_data =  [
    ('RUMAH_SAKIT', 'Rumah Sakit'),
    ('PUSKESMAS', 'Puskesmas'),
    ('KLINIK','klinik')
]

class CreateFaskesForm(forms.Form):
    kode_faskes = forms.CharField(label='Kode Faskes', max_length=3, disabled=True, required=True)
    tipe = forms.ChoiceField(choices=tipe_data, required=True)
    nama_faskes = forms.CharField(label='Nama Faskes', max_length=50, required=True)
    status_kepemilikan = forms.CharField(label='Status Kepemilikan', max_length=30, required=True)

class CreateFaskesAlamatForm(forms.Form):
    jalan = forms.CharField(max_length=30, required=True)
    kelurahan = forms.CharField(max_length=30, required=True)
    kecamatan = forms.CharField(max_length=30, required=True)
    kabupaten_kota = forms.CharField(label='Kabupaten/Kota',max_length=30, required=True)
    provinsi = forms.CharField(max_length=30, required=True)

class DetailFaskesForm(forms.Form):
    kode_faskes = forms.CharField(label='Kode Faskes', max_length=3, disabled=True, required=True)
    tipe = forms.ChoiceField( disabled=True,choices=tipe_data, required=True)
    nama_faskes = forms.CharField(label='Nama Faskes', disabled=True, max_length=50, required=True)
    status_kepemilikan = forms.CharField(label='Status Kepemilikan', disabled=True, max_length=30, required=True)

class DetailFaskesAlamatForm(forms.Form):
    jalan = forms.CharField(max_length=30, disabled=True, required=True)
    kelurahan = forms.CharField(max_length=30, disabled=True, required=True)
    kecamatan = forms.CharField(max_length=30, disabled=True, required=True)
    kabupaten_kota = forms.CharField(label='Kabupaten/Kota',max_length=30, disabled=True, required=True)
    provinsi = forms.CharField(max_length=30, disabled=True, required=True)
