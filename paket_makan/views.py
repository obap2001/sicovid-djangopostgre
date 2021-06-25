from django.shortcuts import render, redirect
from django.http import response
from django.contrib import messages
from django.db import connection
from .forms import CreatePaketMakanForm, UpdatePaketMakanForm

# Create your views here.
def create_paket_makan_view(request):
    if ('username' in request.session and request.session['peran'] == 'ADMIN_SISTEM'):
        response = {}

        form_paket_makan = CreatePaketMakanForm(request.POST or None)
        response['form_paket_makan'] = form_paket_makan

        if request.method == 'POST' and form_paket_makan.is_valid():
            kodeHotel = form_paket_makan.cleaned_data['kodeHotel']
            kodePaket = form_paket_makan.cleaned_data['kodePaket']
            nama = form_paket_makan.cleaned_data['nama']
            harga = form_paket_makan.cleaned_data['harga']

            with connection.cursor() as cursor:
                cursor.execute(f'''
                     INSERT INTO paket_makan values(
                         '{kodeHotel}', '{kodePaket}', '{nama}', '{harga}'
                     );
                ''')
            messages.success(request, f'Paket Makan Berhasil Ditambahkan')
            return redirect('list_paket_makan')
        return render(request, 'create_paket_makan.html', response)

    else:
        return redirect('home')

def list_paket_makan_view(request):
    if 'username' in request.session and (request.session['peran'] == 'ADMIN_SISTEM' or request.session['peran'] == 'ADMIN_SATGAS' or request.session['peran'] == 'PENGGUNA_PUBLIK'):
        response = {} 
        data_paket_makan = []

        with connection.cursor() as cursor:
            cursor.execute(f'''
                 SELECT * FROM paket_makan
                 ORDER BY kodeHotel ASC;
            ''')
            data_paket_makan = cursor.fetchall()
            response['data_paket_makan'] = data_paket_makan

        return render(request, 'list_paket_makan.html', response)

    else:
        return redirect('home')

def delete_paket_makan_view(request, kodePaket):
    if 'username' in request.session and request.session['peran'] == "ADMIN_SISTEM":
        with connection.cursor() as cursor:
            cursor.execute(f'''
                 DELETE from paket_makan
                 WHERE kodePaket = '{kodePaket}' and kodePaket NOT IN
                    (SELECT kodePaket from daftar_pesan)    
                ;
            ''')
        return redirect('list_paket_makan')
    else:
        return redirect('home')

def update_paket_makan_view(request, kodePaket):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SISTEM':
        response = {}
        data_paket_makan = fetch_paket_makan(request, kodePaket)

        if not data_paket_makan:
            messages.error(request, 'Data Paket Makan Tidak Ditemukan')
            return redirect('home')

        form_paket_makan = UpdatePaketMakanForm(request.POST or None, initial=data_paket_makan)

        response['form_paket_makan'] = form_paket_makan

        if request.method == 'POST' and form_paket_makan.is_valid():
            nama = form_paket_makan.cleaned_data['nama']
            harga = form_paket_makan.cleaned_data['harga']

            with connection.cursor() as cursor:
                cursor.execute(f'''
                     UPDATE PAKET_MAKAN
                     SET 
                     nama = '{nama}',
                     harga = {harga}
                     WHERE kodepaket = '{kodePaket}';
                ''')
            
            messages.success(request, 'Data Paket Makan Berhasil Diubah')
            return redirect('list_paket_makan')
        return render(request, 'update_paket_makan.html', response)

    else:
        return redirect('home')

def fetch_paket_makan(request, kodePaket):
    data_paket_makan = []
    with connection.cursor() as cursor:
        cursor.execute(f'''
             SELECT * from paket_makan
             WHERE kodePaket = '{kodePaket}';
        ''')
        data_paket_makan = cursor.fetchone()

    if not data_paket_makan:
        return False

    init_paket_makan_data={
        'kodeHotel' : data_paket_makan[0],
        'kodePaket' : data_paket_makan[1],
        'nama' : data_paket_makan[2],
        'harga' : data_paket_makan[3]
    }

    return init_paket_makan_data