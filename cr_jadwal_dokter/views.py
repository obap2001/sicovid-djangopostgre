from django.http import response
from django.contrib import messages
from django.shortcuts import redirect, render
from django.db import connection, InternalError
from datetime import datetime 

# Create your views here.

def createJadwalDokter(request):
    if 'username' in request.session and request.session['peran'] == 'DOKTER':
        #get data from button
        if request.method == 'GET':
            username = request.GET.get('username')
            kode_faskes = request.GET.get('kode_faskes')
            shift = request.GET.get('shift')
            tanggal = datetime.strptime(request.GET.get('tanggal'), '%B %d, %Y').date()

            # if username is None or kode_faskes is None or shift is None or tanggal is None:
            #     return redirect('cr_jadwal_dokter:list_jadwal_dokter')

            with connection.cursor() as cursor:
                #get nostr from dokter
                cursor.execute(
                    f'''select nostr from dokter
                    where username = '{request.session['username']}';
                    '''
                )
                nostr = cursor.fetchone()[0]

                cursor.execute(
                    f'''select * from jadwal_dokter
                    where nostr = '{nostr}'
                    and username = '{username}'
                    and kode_faskes = '{kode_faskes}'
                    and shift = '{shift}'
                    and tanggal = CAST('{tanggal}' as date);
                    '''
                )

                check_data = cursor.fetchone()

                # if data already exists then skip
                if check_data:
                    return redirect('cr_jadwal_dokter:list_jadwal_dokter')

                # if not add to jadwal_dokter
                cursor.execute(
                    f'''insert into jadwal_dokter values(
                        '{nostr}', '{username}', '{kode_faskes}', '{shift}', CAST('{tanggal}' as date), 0);
                    '''
                )
        return redirect('cr_jadwal_dokter:list_jadwal_dokter')
        
    else:
        return render(request, 'home.html')

def listJadwalDokterSendiri(request):
    if 'username' in request.session and request.session['peran'] == 'DOKTER':
        response_a = {}
        jadwals = [] #init jadwal for all jadwals
        
        #fetch data from JADWAL for table
        with connection.cursor() as cursor:
            cursor.execute(
                f'''select * from jadwal;'''
            )
            jadwals = cursor.fetchall()
            response_a['jadwals'] = jadwals
            print(response_a)

        return render(request,'createjadwaldokter.html', response_a)
        

def listJadwalDokter(request):
    if 'username' in request.session and (request.session['peran'] == 'ADMIN_SATGAS' or request.session['peran'] == 'PENGGUNA_PUBLIK'):
        response = {}
        list_jadwal_dokter = [] #init

        #get jadwal dokter
        with connection.cursor() as cursor:
            cursor.execute(
                f'''select * from jadwal_dokter;
                '''
            )
            list_jadwal_dokter = cursor.fetchall()
            response['list_jadwal_dokter'] = list_jadwal_dokter
        return render(request,'listjadwaldokter.html', response)

    elif 'username' in request.session and request.session['peran']== 'DOKTER':
        response_b = {}
        list_jadwal_dokter_sendiri = [] #init
         #get jadwal dokter
        with connection.cursor() as cursor:
            cursor.execute(
                f'''select * from jadwal_dokter
                where username = '{request.session['username']}';
                '''
            )
            list_jadwal_dokter_sendiri = cursor.fetchall()
            response_b['list_jadwal_dokter_sendiri'] = list_jadwal_dokter_sendiri

        return render(request,'listjadwaldokter.html', response_b)
        
    else:
        return render(request, 'home.html')