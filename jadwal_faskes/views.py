from datetime import datetime
from django.contrib import messages
from django.db import connection
from django.shortcuts import redirect, render
from .forms import CreateJadwalFaskesForm

# Create your views here.
def create_jadwal_faskes_view(request):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SATGAS':
        response = {}

        # Instantiate Form
        form_jadwal = CreateJadwalFaskesForm(request.POST or None)

        # Passing form to response
        response['form_jadwal'] = form_jadwal

        # validate form
        if request.method == 'POST' and form_jadwal.is_valid():
            kode_faskes = form_jadwal.cleaned_data['kode_faskes']
            shift = form_jadwal.cleaned_data['shift']
            tanggal = form_jadwal.cleaned_data['tanggal']
            tanggal = tanggal.strftime('%Y-%m-%d')

            # Insert Data on table
            with connection.cursor() as cursor:
                cursor.execute(f'''
                INSERT INTO jadwal values
                ('{kode_faskes}','{shift}','{tanggal}')
                ''')
            messages.success(request,f'Jadwal Berhasil Ditambahkan')
            return redirect('list_jadwal')

        return render(request,'create_jadwal.html',response)

    else:
        return redirect('home')

def list_jadwal_view(request):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SATGAS':
        response = {}
        data_jadwal = [] #init data_jadwal

        with connection.cursor() as cursor:
            cursor.execute(
                f'SELECT * FROM JADWAL;'
            )
            data_jadwal = cursor.fetchall()
        print(data_jadwal)

        # Reorganize data
        data_organized = []
        id_now = 1
        for i in data_jadwal:
            temp = (id_now, i[0], i[1], i[2].strftime('%d-%m-%Y'))
            data_organized.append(temp)
            id_now += 1
        response['data_jadwal'] = data_organized

        return render(request,'list_jadwal.html', response)

    else:
        return redirect('home')
