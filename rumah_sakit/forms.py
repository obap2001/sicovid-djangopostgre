from tk4_basdat.settings import DATE_INPUT_FORMATS
from django import forms
from django.db import connection

def fetch_data_rs():
    fetch_data_rs = []
    with connection.cursor() as cursor:
        cursor.execute('''
        SELECT F.kode, F.nama from FASKES F
        WHERE F.kode NOT IN (
            SELECT F.KODE from FASKES F, RUMAH_SAKIT RS
            WHERE F.KODE = RS.KODE_FASKES
        );
        ''')
        fetch_data_rs = cursor.fetchall()

    # Organized the data
    data_organized = []
    for i in fetch_data_rs:
        temp = (i[0],f'({i[0]}) {i[1]}')
        data_organized.append(temp)

    return tuple(data_organized)

class CreateRSForm(forms.Form):
    faskes = forms.ChoiceField(choices=fetch_data_rs(), required=True)
    rujukan = forms.BooleanField(required=True)

class UpdateRSForm(forms.Form):
    faskes = forms.ChoiceField(disabled=True,choices=fetch_data_rs(), required=True)
    rujukan = forms.BooleanField(required=True)