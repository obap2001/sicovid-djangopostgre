from django.shortcuts import redirect, render
from django.db import connection
from django.contrib import messages
from .forms import CreateReservasiForm, UpdateReservasiForm

# Create your views here.
def create_reservasi_rs_view(request):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SATGAS':
        response = {}

        form_reservasi = CreateReservasiForm(request.POST or None)
        response['form_reservasi'] = form_reservasi

        if request.method == 'POST' and form_reservasi.is_valid():
            nik = form_reservasi.cleaned_data['nik']
            tanggal_masuk = form_reservasi.cleaned_data['tanggal_masuk'].strftime('%Y-%m-%d')
            tanggal_keluar = form_reservasi.cleaned_data['tanggal_keluar'].strftime('%Y-%m-%d')
            kode_rumah_sakit = form_reservasi.cleaned_data['kode_rumah_sakit']
            kode_ruangan = form_reservasi.cleaned_data['kode_ruangan']
            kode_bed = form_reservasi.cleaned_data['kode_bed']

            with connection.cursor() as cursor:
                    cursor.execute(f'''
                        INSERT INTO RESERVASI_RS VALUES
                        ('{nik}','{tanggal_masuk}','{tanggal_keluar}','{kode_rumah_sakit}','{kode_ruangan}','{kode_bed}')
                    ''')

            messages.success(request, 'Data Reservasi Behasil ditambahkan')
            return redirect('list_reservasi_rs')

        return render(request,'create_reservasi_rs.html',response)
    else:
        return redirect('home')

def list_reservasi_rs_view(request):
    if 'username' in request.session and (request.session['peran'] == 'ADMIN_SATGAS' or request.session['peran'] == 'PENGGUNA_PUBLIK' ):
        response = {}
        data_reservasi = []

        # Fetch Data
        with connection.cursor() as cursor:
            if request.session['peran'] == 'PENGGUNA_PUBLIK':
                cursor.execute(f'''
                SELECT RRS.KodePasien, RRS.tglmasuk, RRS.tglkeluar, RRS.koders, RRS.koderuangan, RRS.kodebed FROM RESERVASI_RS RRS, PASIEN P
                WHERE RRS.kodepasien = P.NIK and p.idpendaftar = '{request.session['username']}';
                ''')
                data_reservasi = cursor.fetchall()

            else:
                cursor.execute(f'''
                SELECT * FROM RESERVASI_RS;
                ''')
                data_reservasi = cursor.fetchall()

        # Reorganized Data
        id_now = 1
        data_organized = []
        for i in data_reservasi:
            temp = (id_now, i[0],i[1].strftime('%d-%m-%Y'), i[2].strftime('%d-%m-%Y'),i[3],i[4],i[5] )
            data_organized.append(temp)
            id_now += 1
        response['data_reservasi'] = data_organized

        return render(request,'list_reservasi_rs.html',response)

    else:
        return redirect('home')

def update_reservasi_rs_view(request,kode_pasien,tanggal):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SATGAS':
        response = {}
        data_reservasi = {} #Init data_pasien
        tanggal_splitted = tanggal.split('-')

        # Fetch Data Reservasi
        with connection.cursor() as cursor:
            cursor.execute(f'''
            SELECT * FROM RESERVASI_RS WHERE
            KODEPASIEN = '{kode_pasien}' AND
            tglmasuk='{tanggal_splitted[2]}-{tanggal_splitted[1]}-{tanggal_splitted[0]}';
            ''')
            data_reservasi = cursor.fetchone()

        init_reservasi= {
            'nik': data_reservasi[0],
            'tanggal_masuk': data_reservasi[1].strftime('%d-%m-%Y'),
            'tanggal_keluar': data_reservasi[2].strftime('%d-%m-%Y'),
            'kode_rumah_sakit': data_reservasi[3],
            'kode_ruangan': data_reservasi[4],
            'kode_bed': data_reservasi[5]
        }

        form_reservasi = UpdateReservasiForm(request.POST or None, initial=init_reservasi)
        response['form_reservasi'] = form_reservasi

        if request.method == 'POST' and form_reservasi.is_valid():
            tanggal_keluar = form_reservasi.cleaned_data['tanggal_keluar']

            with connection.cursor() as cursor:
                    cursor.execute(f'''
                        UPDATE RESERVASI_RS
                        SET tglkeluar = '{tanggal_keluar.strftime('%Y-%m-%d')}'
                        WHERE kodepasien = '{kode_pasien}' and
                        tglmasuk='{tanggal_splitted[2]}-{tanggal_splitted[1]}-{tanggal_splitted[0]}' ;
                    ''')

            messages.success(request, 'Data Reservasi Behasil diubah')
            return redirect('list_reservasi_rs')

        return render(request,'update_reservasi_rs.html',response)

    else:
        return redirect('home')

def delete_reservasi_rs_view(request,kode_pasien,tanggal):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SATGAS':
        # Deleting data in SQL
        tanggal_splitted = tanggal.split('-')
        with connection.cursor() as cursor:
            cursor.execute(
                f'''
                DELETE FROM RESERVASI_RS
                WHERE kodepasien = '{kode_pasien}' and
                tglmasuk='{tanggal_splitted[2]}-{tanggal_splitted[1]}-{tanggal_splitted[0]}';
                '''
            )
            cursor.execute(
                f'''
                DELETE FROM TRANSAKSI_RS
                WHERE kodepasien = '{kode_pasien}' and
                tglmasuk='{tanggal_splitted[2]}-{tanggal_splitted[1]}-{tanggal_splitted[0]}';
                '''
            )
        messages.success(request, f'Data Reservasi berhasil dihapus')
        return redirect('list_reservasi_rs')

    else:
        return redirect('home')


def fetch_data_ruangan(request):
    rs = request.GET.get('rumah_sakit')
    list_ruangan = []

    with connection.cursor() as cursor:
        cursor.execute(f'''
            SELECT koderuangan FROM RUANGAN_RS
            WHERE koders='{rs}' AND jmlbed > 0  ;
        ''')
        list_ruangan = cursor.fetchall()

    # Organized the data
    cleaned_data = []
    for i in list_ruangan:
        temp= (i[0],i[0])
        cleaned_data.append(temp)
    return render(request, 'ruangan_dropdown.html', {'list_ruangan': cleaned_data})

def fetch_data_bed(request):
    rs = request.GET.get('rumah_sakit')
    ruangan = request.GET.get('kode_ruangan')
    list_bed = []

    with connection.cursor() as cursor:
        cursor.execute(f'''
            SELECT kodebed FROM BED_RS
            WHERE koders='{rs}' and koderuangan='{ruangan}';
        ''')
        list_bed = cursor.fetchall()

    # Organized the data
    cleaned_data = []
    for i in list_bed:
        temp= (i[0],i[0])
        cleaned_data.append(temp)
    return render(request, 'bed_dropdown.html', {'list_bed': cleaned_data})
