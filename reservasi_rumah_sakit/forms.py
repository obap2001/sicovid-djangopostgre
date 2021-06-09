from django import forms
from django.db import connection

def fetch_data_faskes():
    faskes_data_choice = []
    with connection.cursor() as cursor:
        cursor.execute(
        'SELECT nik, Nama From NIK;'
        )
        faskes_data_choice = cursor.fetchall() #Will Get all output of the query
    return tuple(faskes_data_choice)

class CreateReservasiForm(forms.Form):
    Nik = forms.ChoiceField(label='NIK')