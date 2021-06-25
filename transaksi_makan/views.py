from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import connection
from .forms import createTransaksiMakanForm, pesananForm

# Create your views here.
def create_transaksi_makan_view(request):
    if ('username' in request.session and request.session['peran'] == 'PENGGUNA_PUBLIK') or ('username' in request.session and request.session['peran'] == 'ADMIN_SATGAS') :
        response = {}

        # Count ID
        id_all = []
        with connection.cursor() as cursor:
            cursor.execute('SELECT idTransaksiMakan FROM transaksi_makan;')
            id_all = cursor.fetchall()

        # Cleaned data
        data_clean = []
        for i in id_all:
            data_clean.append(i[0])

        # Generate all possible id
        id_now = ''
        for i in range(1,100):
            if i < 10 :
                id_now = 'TRM00' + str(i)
            else:
                id_now = 'TRM0' + str(i)

            if id_now not in data_clean:
                break

        #get kode hotel
        kode_hotel_all = []
        with connection.cursor() as cursor:
            cursor.execute(f'''
                SELECT TH.idtransaksi, RH.kodeHotel 
                FROM transaksi_hotel TH JOIN reservasi_hotel RH
                ON TH.kodepasien = RH.kodepasien;
            ''')
            kode_hotel_all = cursor.fetchall()

        #cleaned data
        

        #instantiate form
        initial_data = {'id_transaksi_makan' : id_now}
        form_transmakan = createTransaksiMakanForm(request.POST or None, initial=initial_data)
        form_pesanan = pesananForm(request.POST or None)

        #passing form to response
        response['form_transmakan'] = form_transmakan
        response['form_pesanan'] = form_pesanan

        

        #validate form
        if request.method == 'POST' and form_transmakan.is_valid():
            id_transaksi = form_transmakan.cleaned_data['id_transaksi']
            id_transaksi_makan = form_transmakan.cleaned_data['id_transaksi_makan']
            kode_hotel = form_transmakan.cleaned_data['kode_hotel']
            kode_paket = form_pesanan.cleaned_data['kode_paket']

            #Count totalharga of paket makanan masih perlu diperbaiki (case paket >1)
            list_harga = []
            with connection.cursor() as cursor:
                cursor.execute(f'''
                    SELECT harga FROM paket_Makan
                    WHERE kodeHotel = '{kode_hotel}' AND kodePaket = '{kode_paket}';
                ''')
                list_harga = cursor.fetchall()

            #Insert data on table
            with connection.cursor() as cursor:
                cursor.execute(f'''
                INSERT INTO transaksi_makan values (
                    '{id_transaksi}','{id_transaksi_makan}','{list_harga[0]}'
                );

                ''')
            messages.success(request, f'Transaksi Makana Berhasil ditambahkan')
            return redirect('daftar_transaksi_makan')

        return render(request, 'create_transmakan.html', response)

    else:
        return redirect('home')