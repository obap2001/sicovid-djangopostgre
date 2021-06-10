from tk4_basdat.settings import DATE_INPUT_FORMATS
from django import forms
from django.db import connection

def fetch_data_faskes():
    fetch_data_faskes = []
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT kode, nama from FASKES;'
        )
        fetch_data_faskes = cursor.fetchall()
    return tuple(fetch_data_faskes)


class CreateJadwalFaskesForm(forms.Form):
    kode_faskes = forms.ChoiceField(label='Kode Faskes', choices=fetch_data_faskes(), required=True)
    shift = forms.CharField(max_length=15, required=True)
    tanggal= forms.DateField(required=True, input_formats=DATE_INPUT_FORMATS)