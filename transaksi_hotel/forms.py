from tk4_basdat.settings import DATETIME_INPUT_FORMATS, DATE_INPUT_FORMATS
from django import forms

class UpdateTransaksiForm(forms.Form):
    nik_pasien = forms.CharField(disabled= True,label='NIK Pasien',max_length=20, required=True)
    id_transaksi = forms.CharField(disabled= True,label='Id Transaksi',max_length=10, required=True)
    tanggal_pembayaran = forms.DateField(disabled= True,label='Tanggal Pembayaran', required=True, input_formats=DATE_INPUT_FORMATS)
    waktu_pembayaran = forms.CharField(disabled= True,label='Waktu Pembayaran',required=True)
    total_biaya = forms.IntegerField(disabled= True,label='Total Biaya',required=True)
    status_bayar = forms.CharField(label='Status Bayar',max_length=15, required=True)