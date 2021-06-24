from django.shortcuts import redirect, render
from django.db import connection
from django.contrib import messages
from .forms import UpdateTransaksiForm

# Create your views here.

def list_transaksi_rs_view(request):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SATGAS':
        response = {}
        data_transaksi = []

        # Fetch Data
        with connection.cursor() as cursor:
            cursor.execute(f'''
            SELECT * FROM TRANSAKSI_RS;
            ''')
            data_transaksi = cursor.fetchall()

        # Organized data
        data_organized = []
        for i in data_transaksi:
            temp = []
            if i[2] == None:
                temp = (i[0],i[1], '-', '-',i[4].strftime('%d-%m-%Y'),int_to_currency(i[5]),i[6])
            else:
                temp = (i[0],i[1],i[2].strftime('%d-%m-%Y'),i[3].strftime('%H:%M:%S'),i[4].strftime('%d-%m-%Y'),int_to_currency(i[5]),i[6])
            data_organized.append(temp)

        response['data_transaksi'] = data_organized
        return render(request,'list_transaksi_rs.html',response)

    else:
        return redirect('home')

def update_transaksi_rs_view(request,id):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SATGAS':
        response = {}
        data_transaksi= {} #Init data_pasien

        # Fetch Data Reservasi
        with connection.cursor() as cursor:
            cursor.execute(f'''
            SELECT * FROM TRANSAKSI_RS WHERE
            idtransaksi = '{id}';
            ''')
            data_transaksi= cursor.fetchone()

        init_transaksi= {
            'id_transaksi': data_transaksi[0],
            'kode_pasien': data_transaksi[1],
            'tanggal_pembayaran': data_transaksi[2].strftime('%d-%m-%Y'),
            'waktu_pembayaran': data_transaksi[3].strftime('%d-%m-%Y %H:%M:%S'),
            'tanggal_masuk': data_transaksi[4].strftime('%d-%m-%Y'),
            'total_biaya': data_transaksi[5],
            'status_bayar': data_transaksi[6]
        }

        form_transaksi= UpdateTransaksiForm(request.POST or None, initial=init_transaksi)
        response['form_transaksi'] = form_transaksi

        if request.method == 'POST' and form_transaksi.is_valid():
            status_bayar = form_transaksi.cleaned_data['status_bayar']

            with connection.cursor() as cursor:
                    cursor.execute(f'''
                        UPDATE transaksi_RS
                        SET statusbayar = '{status_bayar}'
                        WHERE idtransaksi = '{id}' ;
                    ''')

            messages.success(request, 'Data transaksi behasil diubah')
            return redirect('list_transaksi_rs')

        return render(request,'update_transaksi_rs.html',response)

    else:
        return redirect('home')


def delete_transaksi_rs_view(request,id):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SATGAS':
        # Deleting data in SQL
        with connection.cursor() as cursor:
            cursor.execute(
                f'''
                DELETE FROM TRANSAKSI_RS
                WHERE idtransaksi = '{id}';
                '''
            )
        messages.success(request, f'Data Transaksi berhasil dihapus')
        return redirect('list_transaksi_rs')

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
