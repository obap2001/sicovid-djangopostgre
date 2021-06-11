from django.db import connection
from django.shortcuts import redirect, render
from .forms import CreatePasienForm, CreatePasienDomisiliAlamatForm, CreatePasienKTPAlamatForm
from .forms import DetailPasienForm, DetailPasienDomisiliAlamatForm, DetailPasienKTPAlamatForm
from .forms import UpdatePasienForm, UpdatePasienDomisiliAlamatForm, UpdatePasienKTPAlamatForm
from django.contrib import messages

# Create your views here.
def create_daftar_pasien_view(request):
    if 'username' in request.session and request.session['peran'] == 'PENGGUNA_PUBLIK':
        response = {}

        # Instantiate Form
        initial_data = {'pendaftar': request.session['username']}
        form_umum = CreatePasienForm(request.POST,initial=initial_data)
        form_KTP = CreatePasienKTPAlamatForm(request.POST)
        form_domisili = CreatePasienDomisiliAlamatForm(request.POST)


        # Passing form to response
        response['form_umum'] = form_umum
        response['form_KTP'] = form_KTP
        response['form_domisili'] = form_domisili

        #Form validation
        if request.method == 'POST' and form_umum.is_valid() and form_KTP.is_valid() and form_domisili.is_valid():
            nik = form_umum.cleaned_data['nik']
            nama = form_umum.cleaned_data['nama']
            nomor_telepon = form_umum.cleaned_data['nomor_telepon']
            nomor_hp = form_umum.cleaned_data['nomor_hp']

            jalan_ktp = form_KTP.cleaned_data['jalan']
            kelurahan_ktp = form_KTP.cleaned_data['kelurahan']
            kecamatan_ktp = form_KTP.cleaned_data['kecamatan']
            kabupaten_kota_ktp = form_KTP.cleaned_data['kabupaten_kota']
            provinsi_ktp = form_KTP.cleaned_data['provinsi']

            jalan_domisili = form_domisili.cleaned_data['jalan']
            kelurahan_domisili = form_domisili.cleaned_data['kelurahan']
            kecamatan_domisili = form_domisili.cleaned_data['kecamatan']
            kabupaten_kota_domisili = form_domisili.cleaned_data['kabupaten_kota']
            provinsi_domisili = form_domisili.cleaned_data['provinsi']

            with connection.cursor() as cursor:
                cursor.execute(
                    f'''SELECT Nama FROM PASIEN where nik='{nik}';'''
                )
                check_exist = cursor.fetchone()
                if check_exist: # Check Record Exist
                    messages.error(request, f'Pasien dengan nama {nama} dan nik {nik} telah terdaftar di database')
                    return redirect('home')
                else:
                    cursor.execute(
                        f'''insert into pasien values
                        ('{nik}','{request.session['username']}','{nama}','{jalan_ktp}','{kelurahan_ktp}','{kecamatan_ktp}','{kabupaten_kota_ktp}','{provinsi_ktp}','{jalan_domisili}','{kelurahan_domisili}','{kecamatan_domisili}','{kabupaten_kota_domisili}','{provinsi_domisili}','{nomor_telepon}','{nomor_hp}')
                        '''
                    )
            messages.success(request, f'Pasien {nama} Berhasil Ditambahkan')
            return redirect('daftar_pasien')

        return render(request,'create_pasien.html',response)
    else:
        return redirect('home')

def list_daftar_pasien_view(request):
    if 'username' in request.session and request.session['peran'] == 'PENGGUNA_PUBLIK':
        response = {}
        data_pasien = [] #Init data_pasien

        # Fetch Pasien Data
        with connection.cursor() as cursor:
            cursor.execute(
                f'SELECT NIK, Nama FROM PASIEN;'
            )
            data_pasien = cursor.fetchall()
            response['data_pasien'] = data_pasien

        #numbering data
        data_pasien_numbered = []
        counter = 1
        for i in data_pasien:
            temp_tuple = (counter, i[0], i[1])
            data_pasien_numbered.append(temp_tuple)
            counter += 1
        response['data'] = data_pasien_numbered

        return render(request,'list_pasien.html',response)
    else:
        return redirect('home')

def detail_daftar_pasien_view(request,nik):
    if 'username' in request.session and request.session['peran'] == 'PENGGUNA_PUBLIK':
        response = {}
        data_pasien = fetch_data_pasien(nik)

        # Check Data Pasien
        if not data_pasien:
            messages.error(request,'Data Pasien Tidak Diemukan')
            return redirect('home')

        # Instantiate Form
        form_umum = DetailPasienForm(request.POST,initial=data_pasien[0])
        form_KTP = DetailPasienKTPAlamatForm(request.POST, initial=data_pasien[1])
        form_domisili = DetailPasienDomisiliAlamatForm(request.POST, initial=data_pasien[2])

        # Passing Form to Temokates
        response['form_umum'] = form_umum
        response['form_KTP'] = form_KTP
        response['form_domisili'] = form_domisili

        return render(request,'detail_pasien.html',response)

    else:
        return redirect('home')

def update_daftar_pasien_view(request,nik):
    if 'username' in request.session and request.session['peran'] == 'PENGGUNA_PUBLIK':
        response = {}
        data_pasien = fetch_data_pasien(nik)

        # Fetch Data Pasien
        if not data_pasien:
            messages.error(request,'Data Pasien Tidak Diemukan')
            return redirect('home')

        # Instantiate Form
        form_umum = UpdatePasienForm(request.POST or None,initial=data_pasien[0])
        form_KTP = UpdatePasienKTPAlamatForm(request.POST or None,initial=data_pasien[1])
        form_domisili = UpdatePasienDomisiliAlamatForm(request.POST or None,initial=data_pasien[2])

        # Passing Form to Templates
        response['form_umum'] = form_umum
        response['form_KTP'] = form_KTP
        response['form_domisili'] = form_domisili

         #Form validation
        if request.method == 'POST' and form_umum.is_valid() and form_KTP.is_valid() and form_domisili.is_valid():
            nomor_telepon = form_umum.cleaned_data['nomor_telepon']
            nomor_hp = form_umum.cleaned_data['nomor_hp']

            jalan_ktp = form_KTP.cleaned_data['jalan']
            kelurahan_ktp = form_KTP.cleaned_data['kelurahan']
            kecamatan_ktp = form_KTP.cleaned_data['kecamatan']
            kabupaten_kota_ktp = form_KTP.cleaned_data['kabupaten_kota']
            provinsi_ktp = form_KTP.cleaned_data['provinsi']

            jalan_domisili = form_domisili.cleaned_data['jalan']
            kelurahan_domisili = form_domisili.cleaned_data['kelurahan']
            kecamatan_domisili = form_domisili.cleaned_data['kecamatan']
            kabupaten_kota_domisili = form_domisili.cleaned_data['kabupaten_kota']
            provinsi_domisili = form_domisili.cleaned_data['provinsi']

            with connection.cursor() as cursor:
                    cursor.execute(f'''
                        UPDATE PASIEN
                        SET ktp_jalan = '{jalan_ktp}',
                        ktp_kelurahan = '{kelurahan_ktp}',
                        ktp_kecamatan = '{kecamatan_ktp}',
                        ktp_kabkot = '{kabupaten_kota_ktp}',
                        ktp_prov = '{provinsi_ktp}',
                        dom_jalan = '{jalan_domisili}',
                        dom_kelurahan = '{kelurahan_domisili}',
                        dom_kecamatan = '{kecamatan_domisili}',
                        dom_kabkot = '{kabupaten_kota_domisili}',
                        dom_prov = '{provinsi_domisili}',
                        notelp = '{nomor_telepon}',
                        nohp = '{nomor_hp}'
                        WHERE nik = '{nik}';
                    ''')

            messages.success(request,'Data Pasien Berhasil diubah')
            return redirect('detail_pasien', nik=nik)

        return render(request,'update_pasien.html',response)

    else:
        return redirect('home')

def delete_daftar_pasien_view(request,nik):
    if 'username' in request.session and request.session['peran'] == 'PENGGUNA_PUBLIK':
        # Deleting data in SQL
        with connection.cursor() as cursor:
            cursor.execute(
                f'''
                DELETE FROM PASIEN
                WHERE NIK = '{nik}';
                '''
            )
        messages.success(request, f'Data Pasien dengan NIK {nik} berhasil dihapus')
        return redirect('daftar_pasien')
    else:
        return redirect('home')

def fetch_data_pasien(nik):
    data_pasien = []
    with connection.cursor() as cursor:
        cursor.execute(
            f'''SELECT * FROM PASIEN where nik='{nik}';'''
        )
        data_pasien = cursor.fetchone()

    # Check if data Exist
    if not data_pasien:
        return False

    # Handling Initial data for form
    init_umum_data = {
        'pendaftar' : data_pasien[1],
        'nik' : data_pasien[0],
        'nama' : data_pasien[2],
        'nomor_telepon' : data_pasien[13],
        'nomor_hp': data_pasien[14]
    }

    init_ktp_data = {
        'jalan'  : data_pasien[3],
        'kelurahan' : data_pasien[4],
        'kecamatan' : data_pasien[5],
        'kabupaten_kota' : data_pasien[6],
        'provinsi' : data_pasien[7]
    }

    init_domisili_data = {
        'jalan'  : data_pasien[8],
        'kelurahan' : data_pasien[9],
        'kecamatan' : data_pasien[10],
        'kabupaten_kota' : data_pasien[11],
        'provinsi' : data_pasien[12]
    }

    return [init_umum_data,init_ktp_data,init_domisili_data]

