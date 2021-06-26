from django import forms
from django.db import connection
from django.http import request

def fetch_data_transaksi_hotel():
    fetch_data_transaksi_hotel = []
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT idtransaksi
            FROM TRANSAKSI_HOTEL;
        ''')
        fetch_data_transaksi_hotel = cursor.fetchall()
    #organnized the data
    data_organized = []
    for i in fetch_data_transaksi_hotel:
        temp = (i[0], f'{i[0]}')
        data_organized.append(temp)

    return tuple(data_organized)

# def fetch_data_reservasi_hotel(id_transaksi_chosen):
#     fetch_data_reservasi_hotel = []
#     with connection.cursor() as cursor:
#         cursor.execute('''
#             SELECT RH.kodePasien, RH.kodeHotel, TH.idtransaksi
#             FROM RESERVASI_HOTEL RH JOIN TRANSAKSI_HOTEL TH
#             ON RH.kodepasien = TH.kodepasien;
#         ''')
#         fetch_data_reservasi_hotel = cursor.fetchall()
#     #organized the data
#     data_organized = []
#     for i in fetch_data_reservasi_hotel:
#         if i[2] == id_transaksi_chosen:
#             temp = (i[1], i[1])
#             data_organized.append(temp)

#     return tuple(data_organized)

# def fetch_data_pesanan(kode_hotel_chosen):
#     fetch_data_pesanan = []
#     with connection.cursor() as cursor:
#         cursor.execute('''
#             SELECT kodeHotel, kodePaket
#             FROM PAKET_MAKAN
#         ''')
#         fetch_data_pesanan = cursor.fetchall()

#     #organize the data
#     data_organized = []
#     for i in fetch_data_pesanan:
#         if i[0] == kode_hotel_chosen:
#             temp = (i[1], i[1])
#             data_organized.append(temp)
#     return tuple(data_organized)

class createTransaksiMakanForm(forms.Form):
    id_transaksi = forms.ChoiceField(choices=fetch_data_transaksi_hotel(), required=True)
    id_transaksi_makan = forms.CharField(max_length=10, disabled=True)
    kode_hotel = forms.CharField(widget=forms.Select(choices=[]), disabled=True)

class pesananForm(forms.Form):
    kode_paket = forms.CharField(widget=forms.Select(choices=[]), required=True)

class DetailTransaksiMakanForm(forms.Form):
    idtransaksi = forms.TimeField(disabled=True)
    idtransaksimakan = forms.CharField(max_length=10, disabled=True)
    kodeHotel = forms.CharField(max_length=5, disabled=True)

class DetailPesananForm(forms.Form):
    id_pesanan = forms.IntegerField(disabled=True)
    kodepaket = forms.CharField(max_length=5, disabled=True)
    harga = forms.IntegerField(disabled=True)
    
class UpdateTransaksiForm(forms.Form):
    idtransaksi = forms.CharField(max_length=10, disabled=True)
    idtransaksimakan = forms.CharField(max_length=10, disabled=True)
    kodeHotel = forms.CharField(max_length=5, disabled=True)

class UpdatePesananForm(forms.Form):
    kodepaket = forms.CharField(max_length=5, required=True)