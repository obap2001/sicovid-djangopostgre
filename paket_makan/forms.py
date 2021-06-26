from django import forms
from django.db import connection
from django.forms.fields import CharField

def fetch_kode_hotel():
    fetch_kode_hotel = []
    with connection.cursor() as cursor:
        cursor.execute(f'''
             SELECT kode from hotel;
        ''')
        fetch_kode_hotel = cursor.fetchall()
    
    #organize the data
    data_organized = []
    for i in fetch_kode_hotel:
        temp = (i[0], f'{i[0]}')
        data_organized.append(temp)

    return tuple(data_organized)

class CreatePaketMakanForm(forms.Form):
    kodeHotel = forms.ChoiceField(choices=fetch_kode_hotel(), required=True)
    kodePaket = forms.CharField(max_length=5, required=True)
    nama = forms.CharField(max_length=20, required=True)
    harga = forms.IntegerField(required=True)

class UpdatePaketMakanForm(forms.Form):
    kodeHotel = forms.ChoiceField(choices=fetch_kode_hotel(), required=True, disabled=True)
    kodePaket = forms.CharField(max_length=5, required=True, disabled=True)
    nama = forms.CharField(max_length=20, required=True)
    harga = forms.IntegerField(required=True)