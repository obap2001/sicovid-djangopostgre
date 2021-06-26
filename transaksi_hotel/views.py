from django.shortcuts import redirect, render
from django.db import connection
from django.contrib import messages
from .forms import UpdateTransaksiForm

# Create your views here.

def list_transaksi_hotel_view(request):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SATGAS':
        response = {}
        data_transaksi = []

        # Fetch Data
        with connection.cursor() as cursor:
            cursor.execute(f'''
            SELECT * FROM TRANSAKSI_HOTEL;
            ''')
            data_transaksi = cursor.fetchall()

        # Organized data
        data_organized = []
        for i in data_transaksi:
            temp = []
            if i[2] == None:
                temp = (i[0],i[1], '-', '-',int_to_currency(i[4]),i[5])
            else:
                temp = (i[0],i[1],i[2].strftime('%d-%m-%Y'),i[3].strftime('%H:%M:%S'),int_to_currency(i[4]),i[5])
            data_organized.append(temp)

        response['data_transaksi'] = data_organized
        return render(request,'list_transaksi_hotel.html',response)

    else:
        return redirect('home')

def int_to_currency(int_value):
    int_value = str(int_value)
    int_value_len = len(int_value)

    result = []
    for i in range(1, int_value_len + 1):
        result.insert(0,int_value[0-i])
        if (i % 3 == 0):
            result.insert(0,".")

    result.insert(0,"Rp ")

    result_str = ''
    for i in result:
        result_str += i

    return result_str

def update_transaksi_hotel_view(request,id):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SATGAS':
        response = {}
        data_transaksi= {} #Init data_pasien

        # Fetch Data Reservasi
        with connection.cursor() as cursor:
            cursor.execute(f'''
            SELECT * FROM TRANSAKSI_HOTEL WHERE
            idtransaksi = '{id}';
            ''')
            data_transaksi= cursor.fetchone()

        init_transaksi= {
            'nik_pasien': data_transaksi[0],
            'id_transaksi': data_transaksi[1],
            'tanggal_pembayaran': data_transaksi[2].strftime('%d-%m-%Y'),
            'waktu_pembayaran': data_transaksi[3].strftime('%d-%m-%Y %H:%M:%S'),
            'total_biaya': data_transaksi[4],
            'status_bayar': data_transaksi[5]
        }

        form_transaksi= UpdateTransaksiForm(request.POST or None, initial=init_transaksi)
        response['form_transaksi'] = form_transaksi

        if request.method == 'POST' and form_transaksi.is_valid():
            status_bayar = form_transaksi.cleaned_data['status_bayar']

            with connection.cursor() as cursor:
                    cursor.execute(f'''
                        UPDATE TRANSAKSI_HOTEL
                        SET statusbayar = '{status_bayar}'
                        WHERE idtransaksi = '{id}' ;
                    ''')

            messages.success(request, 'Data transaksi behasil diubah')
            return redirect('list_transaksi_hotel')

        return render(request,'update_transaksi_hotel.html',response)

    else:
        return redirect('home')

def delete_transaksi_hotel_view(request,id):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SATGAS':
        # Deleting data in SQL
        with connection.cursor() as cursor:
            cursor.execute(
                f'''
                DELETE FROM TRANSAKSI_HOTEL
                WHERE idtransaksi = '{id}';
                '''
            )
        messages.success(request, f'Data Transaksi berhasil dihapus')
        return redirect('list_transaksi_hotel')

    else:
        return redirect('home')