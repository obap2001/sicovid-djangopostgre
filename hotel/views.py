from django.http import response
from django.shortcuts import render, redirect
from django.db import connection
from .forms import CreateAlamatHotelForm, CreateHotelForm
from django.contrib import messages

# Create your views here.
def create_hotel_view(request):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SISTEM':
        response = {}

        kode_all = []
        with connection.cursor() as cursor:
            cursor.execute(f'''
                 SELECT kode FROM HOTEL;
            ''')
            kode_all = cursor.fetchall()

        data_clean = []
        for i in kode_all:
            data_clean.append(i[0])

        kode_now = ''
        for i in range(1,100):
            if i < 10:
               kode_now = 'H0'+str(i)
            else:
                kode_now = 'H' + str(i)
            
            if kode_now not in data_clean:
                break
            
        initial_data =  {'kode' : kode_now}
        form_hotel = CreateHotelForm(request.POST or None, initial=initial_data)
        form_alamat = CreateAlamatHotelForm(request.POST or None)

        response['form_hotel'] = form_hotel
        response['form_alamat'] = form_alamat

        if request.method == 'POST' and form_hotel.is_valid():
            kode = form_hotel.cleaned_data['kode']
            namaHotel = form_hotel.cleaned_data['namaHotel']
            rujukan = form_hotel.cleaned_data['rujukan']
            jalan = form_alamat.cleaned_data['jalan']
            kelurahan = form_alamat.cleaned_data['kelurahan']
            kecamatan = form_alamat.cleaned_data['kecamatan']
            kabupaten = form_alamat.cleaned_data['kabupaten_kota']
            provinsi = form_alamat.cleaned_data['provinsi']

            with connection.cursor() as cursor:
                cursor.execute(f'''
                    INSERT INTO hotel values(
                        '{kode}', '{namaHotel}', 
                        '{rujukan}', '{jalan}', 
                        '{kelurahan}', '{kecamatan}', 
                        '{kabupaten}', '{provinsi}'
                    );
                ''')
            messages.success(request, 'Hotel Berhasil ditambahkan')
            return redirect('daftar_hotel')

        return render(request, 'create_hotel.html', response)
    
    else:
        return redirect('home')



