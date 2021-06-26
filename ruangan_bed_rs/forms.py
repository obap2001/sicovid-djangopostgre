from django import forms
from django.forms import Form, ValidationError
from django.db import connection, transaction, IntegrityError

class form_create_ruanganrs(forms.Form):
	harga_ruangan = forms.CharField(label="Harga Ruangan", required=True, max_length=10, widget=forms.TextInput(attrs={
		'class': 'form-control'}))

	tipe = forms.CharField(label="Tipe", required=True, max_length=10, widget=forms.TextInput(attrs={
		'class': 'form-control'}))   

class form_update_ruanganrs(forms.Form):
	kode_rs = forms.CharField(label='Kode Rumah Sakit', required=False, widget=forms.TextInput(attrs={
		'class': 'form-control',
		'readonly': True}))

	kode_ruangan = forms.CharField(label="Kode Ruangan", required=False, widget=forms.TextInput(attrs={
		'class': 'form-control',
		'readonly': True}))

	harga = forms.CharField(label="Harga Ruangan", required=True, max_length=10, widget=forms.TextInput(attrs={
		'class': 'form-control'}))

	tipe = forms.CharField(label="Tipe", required=True, max_length=10, widget=forms.TextInput(attrs={
		'class': 'form-control'})) 

class form_create_bedrs(forms.Form):
	choices = []

	kode_rs = forms.ChoiceField(label='Kode Rumah Sakit', required=True, choices=choices, widget=forms.Select(attrs={
		'class': 'form-control',
		'id' : 'kode_rs',
		'required' : True}))