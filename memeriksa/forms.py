from django import forms
from django.forms import Form, ValidationError
from django.db import connection, transaction, IntegrityError

class form_create_appointment(forms.Form):
    nikpasien_choices = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with connection.cursor() as cursor:
            cursor.execute(f'''select nik, nik from pasien;''')
            self.fields['nik_pasien'].choices = cursor.fetchall()

    pos_attrs = {
        'class': 'form-control',
    }

    nik_pasien = forms.ChoiceField(label='NIK Pasien', required=True, choices=nikpasien_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    email_dokter = forms.CharField(label="Email Dokter", required=False, widget=forms.TextInput(attrs={'class': 'form-control','readonly': True}))
    kode_faskes = forms.CharField(label="Kode Faskes", required=True, max_length=10, widget=forms.TextInput(attrs={'class': 'form-control','readonly': True}))
    tanggal = forms.CharField(label="Tanggal Praktek", required=True, widget=forms.TextInput(attrs={'class': 'form-control','readonly': True}))   
    shift = forms.CharField(label="Shift Praktek", required=False, widget=forms.TextInput(attrs={'class': 'form-control','readonly': True}))

class form_update_appointment(forms.Form):
	nik_pasien = forms.CharField(label="NIK Pasien", required=False, widget=forms.TextInput(attrs={'class': 'form-control','readonly': True}))
	email_dokter = forms.CharField(label="Email Dokter", required=False, widget=forms.TextInput(attrs={'class': 'form-control','readonly': True}))
	kode_faskes = forms.CharField(label="Kode Faskes", required=False, max_length=10, widget=forms.TextInput(attrs={'class': 'form-control','readonly': True}))
	tanggal = forms.CharField(label="Tanggal Praktek", required=False, widget=forms.TextInput(attrs={'class': 'form-control','readonly': True}))   
	shift = forms.CharField(label="Shift Praktek", required=False, widget=forms.TextInput(attrs={'class': 'form-control','readonly': True}))
	rekomendasi = forms.CharField(label="Rekomendasi", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
