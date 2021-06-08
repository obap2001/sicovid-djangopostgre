from django.db import connection
from django.shortcuts import redirect, render
from .forms import CreatePasienForm, CreatePasienDomisiliAlamatForm, CreatePasienKTPAlamatForm
from .forms import DetailPasienForm, DetailPasienDomisiliAlamatForm, DetailPasienKTPAlamatForm
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

        return render(request,'create_pasien.html',response)
    else:
        return redirect('home')

def read_daftar_pasien_view(request):
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

        return render(request,'read_pasien.html',response)
    else:
        return redirect('home')

def detail_daftar_pasien_view(request,nik):
    if 'username' in request.session and request.session['peran'] == 'PENGGUNA_PUBLIK':
        response = {}

        # Fetch Data Pasien
        data_pasien = []
        with connection.cursor() as cursor:
            cursor.execute(
                f'''SELECT * FROM PASIEN where nik='{nik}';'''
            )
            data_pasien = cursor.fetchone()

        # Check if data Exist
        if not data_pasien:
            messages.error(request,'Data Pasien Tidak Diemukan')
            return redirect('home')

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

        # Instantiate Form
        form_umum = DetailPasienForm(request.POST,initial=init_umum_data)
        form_KTP = DetailPasienKTPAlamatForm(request.POST, initial=init_ktp_data)
        form_domisili = DetailPasienDomisiliAlamatForm(request.POST, initial=init_domisili_data)

        # Passing Form to Temokates
        response['form_umum'] = form_umum
        response['form_KTP'] = form_KTP
        response['form_domisili'] = form_domisili

        return render(request,'detail_pasien.html',response)

    else:
        return redirect('home')

def update_daftar_pasien_view(request,nik):
    pass

def delete_daftar_pasien_view(request,nik):
    pass