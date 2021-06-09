from django.contrib import messages
from django.db import connection
from django.shortcuts import render,redirect
from .forms import CreateFaskesForm,CreateFaskesAlamatForm
from .forms import DetailFaskesAlamatForm, DetailFaskesForm

# Create your views here.
def create_faskes_view(request):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SATGAS':
        response = {}

        # Count ID
        id_now = 0
        with connection.cursor() as cursor:
            cursor.execute('SELECT count(kode) FROM faskes')
            id_now = cursor.fetchone()[0] + 1

        if id_now < 10 :
            id_now = 'F0' + str(id_now)
        else:
            id_now = 'F' + str(id_now)

        # Instantiate Form
        inital_data = {'kode_faskes' : id_now}
        form_umum = CreateFaskesForm(request.POST or None, initial=inital_data)
        form_alamat = CreateFaskesAlamatForm(request.POST or None)

        # Passing form to response
        response['form_umum'] = form_umum
        response['form_alamat'] = form_alamat

        if request.method == 'POST' and form_umum.is_valid() and form_alamat.is_valid():
            kode_faskes = form_umum.cleaned_data['kode_faskes']
            tipe = form_umum.cleaned_data['tipe']
            nama_faskes = form_umum.cleaned_data['nama_faskes']
            status_kepemilikan = form_umum.cleaned_data['status_kepemilikan']

            jalan = form_alamat.cleaned_data['jalan']
            kelurahan = form_alamat.cleaned_data['kelurahan']
            kecamatan = form_alamat.cleaned_data['kecamatan']
            kabupaten_kota = form_alamat.cleaned_data['kabupaten_kota']
            provinsi = form_alamat.cleaned_data['provinsi']

            # Insert Data on table
            with connection.cursor() as cursor:
                cursor.execute(f'''
                INSERT INTO faskes values (
                    '{kode_faskes}','{tipe}','{nama_faskes}','{status_kepemilikan}',
                    '{jalan}','{kelurahan}','{kecamatan}','{kabupaten_kota}','{provinsi}'
                );
                ''')
            messages.success(request,f'Faskes {nama_faskes} Berhasil Ditambahkan')
            return redirect('list_faskes')

        return render(request,'create_faskes.html', response)

    else:
        return redirect('home')

def list_faskes_view(request):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SATGAS':
        response = {}
        data_faskes = [] #Init data_faskes

        # Fetch Pasien Data
        with connection.cursor() as cursor:
            cursor.execute(
                f'SELECT KODE,TIPE,Nama FROM FASKES;'
            )
            data_faskes = cursor.fetchall()
            response['data_faskes'] = data_faskes

        return render(request,'list_faskes.html',response)

    else:
        return redirect('home')

def detail_faskes_view(request,kode):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SATGAS':
        response = {}
        data_faskes = fetch_data_faskes(kode)

        # Check Data_faskes
        if not data_faskes:
            messages.error(request,'Data Faskes Tidak Diemukan')
            return redirect('home')

        #Instantiate Form
        form_umum = DetailFaskesForm(request.POST or None, initial=data_faskes[0])
        form_alamat = DetailFaskesAlamatForm(request.POST or None, initial=data_faskes[1])

        # Passing form to response
        response['form_umum'] = form_umum
        response['form_alamat'] = form_alamat

        return render(request,'detail_faskes.html',response)

    else:
        return redirect('home')


def update_faskes_view(request,kode):
    pass

def delete_faskes_view(request,kode):
    pass

def fetch_data_faskes(kode):
    data_faskes = []
    with connection.cursor() as cursor:
        cursor.execute(
            f'''SELECT * FROM FASKES where KODE='{kode}' '''
        )
        data_faskes = cursor.fetchone()

    if not data_faskes:
        return False

    init_umum_data = {
        'kode_faskes' : data_faskes[0],
        'tipe' : data_faskes[1],
        'nama_faskes' : data_faskes[2],
        'status_kepemilikan' : data_faskes[3]
    }

    init_alamat_data = {
        'jalan'  : data_faskes[4],
        'kelurahan' : data_faskes[5],
        'kecamatan' : data_faskes[6],
        'kabupaten_kota' : data_faskes[7],
        'provinsi' : data_faskes[8]
    }

    return (init_umum_data, init_alamat_data)