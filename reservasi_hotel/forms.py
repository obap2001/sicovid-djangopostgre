from django.core.exceptions import ValidationError
from tk4_basdat.settings import DATE_INPUT_FORMATS
from django import forms
from django.db import connection
import datetime

def fetch_nik_pasien():
    faskes_data_choice = []

    with connection.cursor() as cursor:
        cursor.execute(
        'SELECT NIK From PASIEN;'
        )
        data_reservasi = cursor.fetchall() #Will Get all output of the query


    # Organize the data
    data_organized = []
    for i in data_reservasi:
        temp = (i[0],i[0])
        data_organized.append(temp)

    return tuple(data_organized)

def fetch_kode_hotel():
    faskes_data_choice = []
    with connection.cursor() as cursor:
        cursor.execute(
        'SELECT kode From HOTEL ;'
        )
        faskes_data_choice = cursor.fetchall() #Will Get all output of the query

    # Organized the data
    data_organized = [('','-------')]
    for i in faskes_data_choice:
        temp = (i[0],i[0])
        data_organized.append(temp)

    return tuple(data_organized)

def fetch_data_ruangan(kode_pasien,tanggal):
    data_ruangan = []
    tanggal_splitted = tanggal.split('-')

    with connection.cursor() as cursor:
        cursor.execute(f'''
        SELECT koderoom From RESERVASI_HOTEL WHERE kodepasien='{kode_pasien}' and tglmasuk='{tanggal_splitted[2]}-{tanggal_splitted[1]}-{tanggal_splitted[0]}';
        ''')
        data_ruangan = cursor.fetchall() #Will Get all output of the query
        # SELECT koderoom From RESERVASI_HOTEL WHERE kodepasien='{kode_pasien}' and tglmasuk='{tanggal}';

    # Organized the data
    # data_organized = []
    # for i in data_ruangan:
    #     temp = (i[0],i[0])
    #     data_organized.append(temp)
    # return tuple(data_organized)
    return data_ruangan

class CreateReservasiForm(forms.Form):
    niks = []

    def __init__(self, *args, **kwargs):
        self.peran = kwargs.pop('peran', None)
        self.username = kwargs.pop('username', None)
        super(CreateReservasiForm,self).__init__(*args, **kwargs)
        print(self.peran)
        with connection.cursor() as cursor:
            if self.peran == 'PENGGUNA_PUBLIK':
                cursor.execute(f'''
                SELECT P.nik,P.nik FROM PASIEN P
                WHERE p.idpendaftar = '{self.username}';
                ''')
                data_reservasi = cursor.fetchall()
            else:
                cursor.execute(f'''
                SELECT NIK,NIK FROM PASIEN;
                ''')
                data_reservasi = cursor.fetchall()
                print(data_reservasi)
            self.fields['nik'].choices = data_reservasi
            print("apaaaaaa")
            print(self.fields['nik'].choices)
            print(self.niks)
            print("lulus basdat")

    nik = forms.ChoiceField(label='NIK Pasien',choices=niks,required = True)
    tanggal_masuk = forms.DateField(label="Tanggal Masuk",required=True, input_formats=DATE_INPUT_FORMATS)
    tanggal_keluar = forms.DateField(label="Tanggal Keluar",required=True, input_formats=DATE_INPUT_FORMATS)
    kode_hotel = forms.ChoiceField(label='Kode Hotel',choices=fetch_kode_hotel(),required = True)
    kode_ruangan = forms.CharField(label="Kode Ruangan", widget=forms.Select(choices=[]), required=True)
    
    def clean(self):
        form_data = self.cleaned_data
        if form_data['tanggal_keluar'] <= form_data['tanggal_masuk']:
            raise ValidationError('Tanggal Keluar tidak boleh kurang dari Tanggal Masuk')

class UpdateReservasiForm(forms.Form):
    initial = {}
    temps = tuple()
    # kode_pasien = ''
    # tanggal = ''
    def __init__(self, *args, **kwargs):
        super(UpdateReservasiForm,self).__init__(*args, **kwargs)
        self.initial = kwargs['initial']
        print(self.initial)
        # self.kode_pasien = kwargs.pop('kode_pasien', None)
        # self.tanggal = kwargs['tanggal']
        self.temp = fetch_data_ruangan(kode_pasien=self.initial['nik'],tanggal=self.initial['tanggal_masuk'])
        print(self.temp)

    nik = forms.ChoiceField(disabled=True, label='NIK Pasien',choices=fetch_nik_pasien(),required = True)
    tanggal_masuk = forms.DateField(disabled=True,label="Tanggal Masuk",required=True, input_formats=DATE_INPUT_FORMATS)
    tanggal_keluar = forms.DateField(label="Tanggal Keluar",required=True, input_formats=DATE_INPUT_FORMATS)
    hotel = forms.ChoiceField(disabled=True,label="Hotel", choices=fetch_kode_hotel(), required=True)
    ruangan = forms.ChoiceField(disabled=True,label="Ruangan", choices=temps, required=True)

    def clean(self):
        form_data = self.cleaned_data
        if form_data['tanggal_keluar'] <= form_data['tanggal_masuk']:
            raise ValidationError('Tanggal Keluar tidak boleh kurang dari Tanggal Masuk')