from django.shortcuts import redirect, render
from django.db import connection
from .forms import CreateReservasiForm, UpdateReservasiForm, DetailReservasiForm

# Create your views here.
def create_reservasi_rs_view(request):
    pass

def list_reservasi_rs_view(request):
    if 'username' in request.session and (request.session['peran'] == 'ADMIN_SATGAS' or request.session['peran'] == 'PENGGUNA_PUBLIK' ):
        response = {}
        data_reservasi = []

        # Fetch Data
        with connection.cursor() as cursor:
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
        return render('home')

def detail_reservasi_rs_view(request,kode_pasien,tanggal):
    pass

def update_reservasi_rs_view(request,kode_pasien,tanggal):
    pass

def delete_reservasi_rs_view(request,kode_pasien,tanggal):
    pass



def fetch_data_ruangan(request):
    rs = request.GET.get('rumah_sakit')
    list_ruangan = []

    with connection.cursor() as cursor:
        cursor.execute(f'''
            SELECT koderuangan FROM RUANGAN_RS
            WHERE koders='{rs}';
        ''')
        list_ruangan = cursor.fetchall()

    # Organized the data
    cleaned_data = []
    for i in list_ruangan:
        temp= (i[0],i[0])
        cleaned_data.append(temp)
    return render(request, 'ruangan_dropdown.html', {'list_ruangan': cleaned_data})

