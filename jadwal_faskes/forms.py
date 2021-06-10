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

    # Organized the data
    data_organized = []
    for i in fetch_data_faskes:
        temp = (i[0],f'({i[0]}) {i[1]}')
        data_organized.append(temp)

    return tuple(data_organized)


class CreateJadwalFaskesForm(forms.Form):
    faskes = forms.ChoiceField(choices=fetch_data_faskes(), required=True)
    shift = forms.CharField(max_length=15, required=True)
    tanggal= forms.DateField(required=True, input_formats=DATE_INPUT_FORMATS)