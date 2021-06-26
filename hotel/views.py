from django.http import response
from django.shortcuts import render, redirect
from django.db import connection
from .forms import CreateAlamatHotelForm, CreateHotelForm
from .forms import FormUpdateHotel, FormUpdateAlamatHotel
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

        if request.method == 'POST' and form_hotel.is_valid() and form_alamat.is_valid():
            kode = form_hotel.cleaned_data['kode']
            namaHotel = form_hotel.cleaned_data['namaHotel']
            rujukan = form_hotel.cleaned_data['rujukan']
            rujukanfinal = int(rujukan)
            jalan = form_alamat.cleaned_data['jalan']
            kelurahan = form_alamat.cleaned_data['kelurahan']
            kecamatan = form_alamat.cleaned_data['kecamatan']
            kabupaten = form_alamat.cleaned_data['kabupaten_kota']
            provinsi = form_alamat.cleaned_data['provinsi']

            with connection.cursor() as cursor:
                cursor.execute(f'''
                    INSERT INTO hotel values(
                        '{kode}', '{namaHotel}', 
                        '{rujukanfinal}', '{jalan}', 
                        '{kelurahan}', '{kecamatan}', 
                        '{kabupaten}', '{provinsi}'
                    );
                ''')
            messages.success(request, 'Hotel Berhasil ditambahkan')
            return redirect('list_hotel')

        return render(request, 'create_hotel.html', response)
    
    else:
        return redirect('home')

def list_hotel_view(request):
    if 'username' in request.session and (request.session['peran'] == 'ADMIN_SISTEM' or request.session['peran'] == 'PENGGUNA_PUBLIK' or request.session['peran'] == 'ADMIN_SATGAS'):
        response = {}
        data_hotel = []

        with connection.cursor() as cursor:
            cursor.execute(f'''
                 SELECT kode, nama, isrujukan, jalan, kelurahan, kecamatan, kabkot, prov
                 FROM hotel
                 ORDER BY kode ASC;
            ''')
            data_hotel = cursor.fetchall()

        cleaned_data = []
        angka = 1
        for i in data_hotel:
            temp = (f'{i[0]}',f'{i[1]}',f'{i[2]}',f'{i[3]}',f'{i[4]}',f'{i[5]}',f'{i[6]}',f'{i[7]}', angka)
            cleaned_data.append(temp)
            angka+=1

        response['data_hotel'] = cleaned_data
         
        return render(request, 'list_hotel.html', response)

    else:
        return redirect('home')

def update_hotel_view(request, kode):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SISTEM':
        response = {}
        data_hotel = {}

        with connection.cursor() as cursor:
            cursor.execute(f'''
                 SELECT * FROM hotel
                 WHERE kode = '{kode}';
            ''')
            data_hotel = cursor.fetchone()

        init_hotel={
            'kode' : data_hotel[0],
            'nama' : data_hotel[1],
            'rujukan' : data_hotel[2],
        }
        init_alamat={
            'jalan' : data_hotel[3],
            'kelurahan' : data_hotel[4],
            'kecamatan' : data_hotel[5],
            'kabupaten_kota' : data_hotel[6],
            'provinsi' : data_hotel[7]
        }

        form_hotel = FormUpdateHotel(request.POST or None, initial=init_hotel)
        form_alamat = FormUpdateAlamatHotel(request.POST or None, initial=init_alamat)

        response['form_hotel'] = form_hotel
        response['form_alamat'] = form_alamat

        if request.method == 'POST' and form_alamat.is_valid() and form_hotel.is_valid():
            nama = form_hotel.cleaned_data['nama']
            rujukan = form_hotel.cleaned_data['rujukan']
            rujukanint = int(rujukan)
            jalan = form_alamat.cleaned_data['jalan']
            kelurahan = form_alamat.cleaned_data['kelurahan']
            kecamatan = form_alamat.cleaned_data['kecamatan']
            kabupaten_kota = form_alamat.cleaned_data['kabupaten_kota']
            provinsi = form_alamat.cleaned_data['provinsi']
            
            with connection.cursor() as cursor:
                cursor.execute(f'''
                     UPDATE hotel
                     SET nama = '{nama}', isrujukan = '{rujukanint}',
                     jalan = '{jalan}', kelurahan = '{kelurahan}',
                     kecamatan = '{kecamatan}', kabkot = '{kabupaten_kota}',
                     prov = '{provinsi}'
                     WHERE kode = '{kode}';
                ''')

            messages.success(request, 'Data Hotel Berhasil Diubah')
            return redirect('list_hotel')

        return render(request, 'update_hotel.html', response)

    else:
        return redirect('home')
