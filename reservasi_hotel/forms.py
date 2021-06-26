from django.core.exceptions import ValidationError
from tk4_basdat.settings import DATE_INPUT_FORMATS
from django import forms
from django.db import connection

def fetch_nik_pasien(peran,username):
    faskes_data_choice = []

    with connection.cursor() as cursor:
            if peran == 'PENGGUNA_PUBLIK':
                cursor.execute(f'''
                SELECT P.nik FROM PASIEN P
                WHERE p.idpendaftar = '{username}';
                ''')
                data_reservasi = cursor.fetchall()

            else:
                cursor.execute(f'''
                SELECT NIK FROM PASIEN;
                ''')
                data_reservasi = cursor.fetchall()

    # Organized the data
    data_organized = []
    for i in data_reservasi:
        temp = (i[0],i[0])
        data_organized.append(temp)

    return tuple(data_organized)

def fetch_kode_hotel():
    faskes_data_choice = []
    with connection.cursor() as cursor:
        cursor.execute(
        'SELECT kode From HOTEL;'
        )
        faskes_data_choice = cursor.fetchall() #Will Get all output of the query

    # Organized the data
    data_organized = [('','-------')]
    for i in faskes_data_choice:
        temp = (i[0],i[0])
        data_organized.append(temp)

    return tuple(data_organized)

def fetch_data_ruangan():
    faskes_data_choice = []
    with connection.cursor() as cursor:
        cursor.execute(
        'SELECT koderoom From HOTEL_ROOM;'
        )
        faskes_data_choice = cursor.fetchall() #Will Get all output of the query

    # Organized the data
    data_organized = []
    for i in faskes_data_choice:
        temp = (i[0],i[0])
        data_organized.append(temp)
    return tuple(data_organized)

class CreateReservasiForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self._peran = kwargs.pop('peran', None)
        self._username = kwargs.pop('username', None)
        super().__init__(*args, **kwargs)

    def peran_username(self):
        peran = self._peran
        username = self._username

    nik = forms.ChoiceField(label='NIK Pasien',choices=fetch_nik_pasien(peran=peran,username=username),required = True)
    tanggal_masuk = forms.DateField(label="Tanggal Masuk",required=True, input_formats=DATE_INPUT_FORMATS)
    tanggal_keluar = forms.DateField(label="Tanggal Keluar",required=True, input_formats=DATE_INPUT_FORMATS)
    kode_hotel = forms.ChoiceField(label='Kode Hotel',choices=fetch_kode_hotel(),required = True)
    kode_ruangan = forms.CharField(label="Kode Ruangan", widget=forms.Select(choices=[]), required=True)
    
    def clean(self):
        form_data = self.cleaned_data
        if form_data['tanggal_keluar'] <= form_data['tanggal_masuk']:
            raise ValidationError('Tanggal Keluar tidak boleh kurang dari Tanggal Masuk')

class UpdateReservasiForm(forms.Form):
    nik = forms.ChoiceField(disabled=True, label='NIK Pasien',choices=fetch_nik_pasien(),required = True)
    tanggal_masuk = forms.DateField(disabled=True,label="Tanggal Masuk",required=True, input_formats=DATE_INPUT_FORMATS)
    tanggal_keluar = forms.DateField(label="Tanggal Keluar",required=True, input_formats=DATE_INPUT_FORMATS)
    hotel = forms.ChoiceField(disabled=True,label="Hotel", choices=fetch_kode_hotel(), required=True)
    ruangan = forms.ChoiceField(disabled=True,label="Ruangan", choices=fetch_data_ruangan(), required=True)

    def clean(self):
        form_data = self.cleaned_data
        if form_data['tanggal_keluar'] <= form_data['tanggal_masuk']:
            raise ValidationError('Tanggal Keluar tidak boleh kurang dari Tanggal Masuk')