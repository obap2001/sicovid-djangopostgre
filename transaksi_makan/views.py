from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import connection
from .forms import createTransaksiMakanForm

# Create your views here.
def create_transaksi_makan_view(request):
    if ('username' in request.session and request.session['peran'] == 'PENGGUNA_PUBLIK') or ('username' in request.session and request.session['peran'] == 'ADMIN_SATGAS') :
        response = {}

        #instantiate form
        form_transmakan = createTransaksiMakanForm(request.POST or None)

        #passing form to response
        response['form_transmakan'] = form_transmakan

        #validate form
        if request.method == 'POST' and form_transmakan.is_valid():
            id_transaksi = form_transmakan.cleaned_data['id_transaksi']
            id_transaksi_hotel = form_transmakan.cleaned_data['id_transaksi_hotel']
            kode_hotel = form_transmakan.cleaned_data['kode_hotel']
            kode_paket = form_transmakan.cleaned_data['kode_paket']
        