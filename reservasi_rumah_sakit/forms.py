from django.core.exceptions import ValidationError
from tk4_basdat.settings import DATE_INPUT_FORMATS
from django import forms
from django.db import connection

def fetch_data_rs():
    faskes_data_choice = []
    with connection.cursor() as cursor:
        cursor.execute(
        'SELECT kode_faskes From RUMAH_SAKIT;'
        )
        faskes_data_choice = cursor.fetchall() #Will Get all output of the query

    # Organized the data
    data_organized = []
    for i in faskes_data_choice:
        temp = (i[0],i[0])
        data_organized.append(temp)

    return tuple(data_organized)

def fetch_data_ruangan_rs():
    faskes_data_choice = []
    with connection.cursor() as cursor:
        cursor.execute(
        'SELECT koders From RUANGAN_RS;'
        )
        faskes_data_choice = cursor.fetchall() #Will Get all output of the query

    # Organized the data
    data_organized = []
    for i in faskes_data_choice:
        temp = (i[0],i[0])
        data_organized.append(temp)

    return tuple(data_organized)

def fetch_data_bed_rs():
    faskes_data_choice = []
    with connection.cursor() as cursor:
        cursor.execute(
        'SELECT KODEBED From BED_RS;'
        )
        faskes_data_choice = cursor.fetchall() #Will Get all output of the query

    # Organized the data
    data_organized = []
    for i in faskes_data_choice:
        temp = (i[0],i[0])
        data_organized.append(temp)
    return tuple(data_organized)

class CreateReservasiForm(forms.Form):
    nik = forms.ChoiceField(label='NIK Pasien',required = True)
    tanggal_masuk = forms.DateField(label="Tanggal Masuk",required=True, input_formats=DATE_INPUT_FORMATS)
    tanggal_keluar = forms.DateField(label="Tanggal Keluar",required=True, input_formats=DATE_INPUT_FORMATS)
    kode_rumah_sakit = forms.ChoiceField(label="Kode Rumah Sakit", choices=fetch_data_ruangan_rs(), required=True)
    kode_ruangan = forms.ChoiceField(label="Kode Ruangan", choices=(), required=True)
    kode_bed = forms.ChoiceField(label="Kode Bed", choices=(), required=True)

    def clean(self):
        form_data = self.cleaned_data
        if form_data['tanggal_keluar'] <= form_data['tanggal_masuk']:
            raise ValidationError('Tanggal Keluar tidak boleh kurang dari Tanggal_masuk')

class UpdateReservasiForm(forms.Form):
    nik = forms.ChoiceField(disabled=True, label='NIK Pasien',required = True)
    tanggal_masuk = forms.DateField(disabled=True,label="Tanggal Masuk",required=True, input_formats=DATE_INPUT_FORMATS)
    tanggal_keluar = forms.DateField(label="Tanggal Keluar",required=True, input_formats=DATE_INPUT_FORMATS)
    kode_rumah_sakit = forms.ChoiceField(disabled=True,label="Kode Rumah Sakit", choices=fetch_data_ruangan_rs(), required=True)
    kode_ruangan = forms.ChoiceField(disabled=True,label="Kode Ruangan", choices=fetch_data_ruangan_rs, required=True)
    kode_bed = forms.ChoiceField(disabled=True,label="Kode Bed", choices=fetch_data_bed_rs, required=True)

class DetailReservasiForm(forms.Form):
    nik = forms.ChoiceField(disabled=True, label='NIK Pasien',required = True)
    tanggal_masuk = forms.DateField(disabled=True, label="Tanggal Masuk", required=True, input_formats=DATE_INPUT_FORMATS)
    tanggal_keluar = forms.DateField(disabled=True, label="Tanggal Keluar", required=True, input_formats=DATE_INPUT_FORMATS)
    kode_rumah_sakit = forms.ChoiceField(disabled=True, label="Kode Rumah Sakit", choices=fetch_data_ruangan_rs(), required=True)
    kode_ruangan = forms.ChoiceField(disabled=True, label="Kode Ruangan", choices=fetch_data_ruangan_rs, required=True)
    kode_bed = forms.ChoiceField(disabled=True, label="Kode Bed", choices=fetch_data_bed_rs, required=True)





