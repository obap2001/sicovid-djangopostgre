from django.shortcuts import redirect, render
from django.db import connection
from django.contrib import messages

# Create your views here.

def list_transaksi_booking_view(request):
    if 'username' in request.session and (request.session['peran'] == 'ADMIN_SATGAS' or request.session['peran'] == 'PENGGUNA_PUBLIK' ):
        response = {}
        data_booking = []

        # Fetch Data
        with connection.cursor() as cursor:
            cursor.execute(f'''
            SELECT * FROM TRANSAKSI_BOOKING;
            ''')
            data_booking = cursor.fetchall()

        # Reorganized Data
        id_now = 1
        data_organized = []
        for i in data_booking:
            temp = (id_now, i[0],i[1],i[2],i[3].strftime('%d-%m-%Y'))
            data_organized.append(temp)
            id_now += 1
        response['data_booking'] = data_organized

        return render(request,'list_transaksi_booking.html',response)

    else:
        return redirect('home')