from django.core.exceptions import ValidationError
from tk4_basdat.settings import DATE_INPUT_FORMATS
from django import forms
from django.db import connection

def fetch_kode_hotel():
    data_choise = []
    with connection.cursor() as cursor:
        cursor.execute(
        'SELECT KODE From HOTEL;'
        )
        data_choice = cursor.fetchall() #Will Get all output of the query

    # Organized the data
    data_organized = []
    for i in data_choice:
        temp = (i[0],i[0])
        data_organized.append(temp)

    return tuple(data_organized)

class CreateRuanganHotelForm(forms.Form):
    kode_hotel = forms.ChoiceField(label='Kode Hotel', choices=fetch_kode_hotel(), required=True)
    kode_ruangan = forms.CharField(disabled=True,label='Kode Ruangan', max_length=5, required=True)
    jenis_bed = forms.CharField(label='Jenis Bed', max_length=50, required=True)
    tipe = forms.CharField(label='Tipe', max_length=50, required=True)
    harga_per_hari = forms.IntegerField(label='Harga per hari', required=True)

class UpdateRuanganHotelForm(forms.Form):
    kode_hotel = forms.ChoiceField(disabled=True, label='Kode Hotel', choices=fetch_kode_hotel(), required=True)
    kode_ruangan = forms.CharField(disabled=True,label='Kode Ruangan', max_length=5, required=True)
    jenis_bed = forms.CharField(label='Jenis Bed', max_length=50, required=True)
    tipe = forms.CharField(label='Tipe', max_length=50, required=True)
    harga_per_hari = forms.IntegerField(label='Harga per hari', required=True)
