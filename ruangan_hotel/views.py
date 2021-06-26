from django.shortcuts import redirect, render
from django.db import connection
from django.contrib import messages
from .forms import CreateRuanganHotelForm, UpdateRuanganHotelForm

# Create your views here.
def create_ruangan_hotel_view(request):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SISTEM':
        response = {}

        # Count ID
        id_all = []
        with connection.cursor() as cursor:
            cursor.execute('SELECT koderoom FROM HOTEL_ROOM')
            id_all = cursor.fetchall()

        # Cleaned data
        data_clean = []
        for i in id_all:
            data_clean.append(i[0])

        # Generate all possible id
        id_now = ''
        for i in range(1,1000):
            if i < 10 :
                id_now = 'RH00' + str(i)
            elif i<100 :
                id_now = 'RH0' + str(i)
            else:
                id_now = 'RH' + str(i)

            if id_now not in data_clean:
                break

        # Instantiate Form
        inital_data = {'kode_ruangan' : id_now}
        form_create_ruangan = CreateRuanganHotelForm(request.POST or None, initial=inital_data)

        # Passing form to response
        response['form_create_ruangan'] = form_create_ruangan

        if request.method == 'POST' and form_create_ruangan.is_valid():
            kode_hotel = form_create_ruangan.cleaned_data['kode_hotel']
            kode_ruangan = form_create_ruangan.cleaned_data['kode_ruangan']
            jenis_bed = form_create_ruangan.cleaned_data['jenis_bed']
            tipe = form_create_ruangan.cleaned_data['tipe']
            harga_per_hari = form_create_ruangan.cleaned_data['harga_per_hari']

            with connection.cursor() as cursor:
                    cursor.execute(f'''
                        INSERT INTO HOTEL_ROOM VALUES
                        ('{kode_hotel}','{kode_ruangan}','{jenis_bed}','{tipe}','{harga_per_hari}')
                    ''')

            messages.success(request, 'Data Ruangan Hotel Behasil ditambahkan')
            return redirect('list_ruangan_hotel')

        return render(request,'create_ruangan_hotel.html',response)
    else:
        return redirect('home')

def list_ruangan_hotel_view(request):
    if 'username' in request.session and (request.session['peran'] == 'ADMIN_SISTEM' or request.session['peran'] == 'ADMIN_SATGAS' or request.session['peran'] == 'PENGGUNA_PUBLIK' ):
        response = {}
        data_ruangan_hotel = []

        # Fetch Data
        with connection.cursor() as cursor:
            cursor.execute(f'''
            SELECT * FROM HOTEL_ROOM;
            ''')
            data_ruangan_hotel = cursor.fetchall()

        # Reorganized Data
        id_now = 1
        data_organized = []
        for i in data_ruangan_hotel:
            temp = (id_now, i[0],i[1],i[2],i[3],i[4])
            data_organized.append(temp)
            id_now += 1
        response['data_ruangan_hotel'] = data_organized

        return render(request,'list_ruangan_hotel.html',response)

    else:
        return redirect('home')

def update_ruangan_hotel_view(request,kode_hotel,kode_ruangan):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SISTEM':
        response = {}
        data_ruangan_hotel = {} #Init data_pasien
        
        # Fetch Data Reservasi
        with connection.cursor() as cursor:
            cursor.execute(f'''
            SELECT * FROM HOTEL_ROOM WHERE
            kodehotel = '{kode_hotel}' AND
            koderoom = '{kode_ruangan}';
            ''')
            data_ruangan_hotel = cursor.fetchone()

        init_ruangan = {
            'kode_hotel': data_ruangan_hotel[0],
            'kode_ruangan': data_ruangan_hotel[1],
            'jenis_bed': data_ruangan_hotel[2],
            'tipe': data_ruangan_hotel[3],
            'harga_per_hari': data_ruangan_hotel[4]
        }

        form_ruangan_hotel = UpdateRuanganHotelForm(request.POST or None, initial=init_ruangan)
        response['form_ruangan_hotel'] = form_ruangan_hotel

        if request.method == 'POST' and form_ruangan_hotel.is_valid():

            with connection.cursor() as cursor:
                    cursor.execute(f'''
                        UPDATE HOTEL_ROOM
                        SET jenisbed = '{jenis_bed}',
                        tipe = '{tipe}',
                        harga = '{harga_per_hari}'
                        WHERE kodehotel = '{kode_hotel}' AND
                        koderoom = '{kode_ruangan}';
                    ''')

            messages.success(request, 'Data Ruangan Hotel Behasil diubah')
            return redirect('list_ruangan_hotel')

        return render(request,'update_ruangan_hotel.html',response)

    else:
        return redirect('home')

def delete_ruangan_hotel_view(request,kode_hotel,kode_ruangan):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SISTEM':

        with connection.cursor() as cursor:
            cursor.execute(
                f'''
                DELETE FROM HOTEL_ROOM
                WHERE kodehotel = '{kode_hotel}' AND
                koderoom = '{kode_ruangan}';
                '''
            )
        messages.success(request, f'Data Ruangan Hotel berhasil dihapus')
        return redirect('list_ruangan_hotel')

    else:
        return redirect('home')