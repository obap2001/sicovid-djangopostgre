from django.http import response
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import connection, InternalError
from datetime import datetime 
from .forms import form_create_appointment, form_update_appointment

# Create your views here.

def createAppointment(request):
    if 'username' in request.session and (request.session['peran'] == 'PENGGUNA_PUBLIK' or request.session['peran'] == 'ADMIN_SATGAS'):
        response = {} #init for response data
        available_scheds = [] #init for all available jadwal
        
        with connection.cursor() as cursor:
            cursor.execute(f'''
            select * from jadwal_dokter;
            '''
            )
            available_scheds = cursor.fetchall()
            response['available_scheds'] = available_scheds
                
        return render(request, "createappointment.html", response)

    else:
        return render(request, 'home.html')

def formAppointment(request):
    if 'username' in request.session and (request.session['peran'] == 'PENGGUNA_PUBLIK' or request.session['peran'] == 'ADMIN_SATGAS'):
        if request.method == 'POST':
            nik_pasien = request.POST['nik_pasien']
            username = request.POST['email_dokter']
            kode_faskes = request.POST['kode_faskes']
            shift = request.POST['shift']
            tanggal = request.POST['tanggal']
            rekomendasi = '-' 

            # get data from table as auto-fill for form 
            data = {'email_dokter': username, 
            'kode_faskes': kode_faskes, 
            'tanggal': tanggal,
            'shift': shift}

            with connection.cursor() as cursor:
                cursor.execute(f'''
                select nostr from dokter
                where username='{username}' 
                LIMIT 1;
                ''')
                no_str = cursor.fetchone()[0]

            try:
                with connection.cursor() as cursor:
                    cursor.execute(f'''
                    insert into memeriksa values(
                    '{nik_pasien}', '{no_str}', '{username}', '{kode_faskes}', '{shift}', '{tanggal}', '{rekomendasi}');
                    ''')
                return redirect('memeriksa:list_appointment')
            except:
                form = form_create_appointment(initial=data)
                context = {'form':form, 'message':'Silahkan pilih shift dan tanggal lainnya, karena shift dan tanggal yang dipilih sudah penuh'}
                return render(request, 'formappointment.html', context)
                
        elif request.method == 'GET':
            username = request.GET.get('username')
            kode_faskes = request.GET.get('kode_faskes')
            shift = request.GET.get('shift')
            tanggal = request.GET.get('tanggal') 

            data = {'email_dokter': username, 
            'kode_faskes': kode_faskes, 
            'tanggal': tanggal,
            'shift': shift}

            form = form_create_appointment(initial=data)
        context = {'form': form}
        return render(request, "formappointment.html", context)
    
    else:
        return render(request, 'home.html')

def listAppointment(request):
    if 'username' in request.session: #authenticated
        response = {} #init for context/response call
        getdata = [] #init for data

        # if user's role is admin satgas, show everything from MEMERIKSA
        if request.session['peran'] == "ADMIN_SATGAS":
            with connection.cursor() as cursor:
                cursor.execute(f'''
                select * from memeriksa;
                ''')
                getdata = cursor.fetchall()

        #if user's role is pengguna publik, show data of patients they registered
        elif request.session['peran'] == "PENGGUNA_PUBLIK":
            with connection.cursor() as cursor:
                cursor.execute(f'''
                select * from memeriksa m 
                join pasien p on 
                m.nik_pasien = p.nik 
                where p.idpendaftar = '{request.session['username']}';
                ''')
                getdata = cursor.fetchall()
        
        #if user's role is dokter, show data of patients they're assigned to
        elif request.session['peran'] == "DOKTER":
            with connection.cursor() as cursor:
                cursor.execute(f'''
                select * from memeriksa 
                where username_dokter = '{request.session['username']}';
                ''')
                getdata = cursor.fetchall()
            
        response['getdata'] = getdata
        return render(request, "listappointment.html", response)
   
    else:
        return render(request, 'home.html')

def updateAppointment(request):
    if 'username' in request.session and request.session['peran'] == 'DOKTER': #authenticate
        if request.method == 'POST':
            nik_pasien = request.POST['nik_pasien']
            username = request.POST['email_dokter']
            kode_faskes = request.POST['kode_faskes']
            shift = request.POST['shift']
            tanggal = request.POST['tanggal']
            rekomendasi = request.POST['rekomendasi']
            
            with connection.cursor() as cursor:
                cursor.execute(f'''
                select nostr from dokter 
                where username = '{username}'
                limit 1;
                ''')
                no_str = cursor.fetchone()[0]
                print(no_str)

            with connection.cursor() as cursor:
                cursor.execute("SET search_path to SIRUCO")
                cursor.execute(
                f'''
                update memeriksa
                set rekomendasi = '{rekomendasi}'
                where nik_pasien = '{nik_pasien}' and
                username_dokter = '{username}' and
                nostr = '{no_str}' and
                kode_faskes = '{kode_faskes}' and
                praktek_shift = '{shift}' and
                praktek_tgl = '{tanggal}';
                ''')
            return redirect('memeriksa:list_appointment')

        elif request.method == 'GET': #from 'update' button click in listappointment
            nik_pasien = request.GET.get('nik_pasien')
            username = request.GET.get('username')
            kode_faskes = request.GET.get('kode_faskes')
            shift = request.GET.get('shift')
            tanggal = request.GET.get('tanggal') 

            data = {
            'nik_pasien': nik_pasien,
            'email_dokter': username, 
            'kode_faskes': kode_faskes, 
            'tanggal': tanggal,
            'shift': shift
            }

            #get no_str from tabel DOKTER
            with connection.cursor() as cursor:
                cursor.execute(f'''
                select nostr from dokter
                where username = '{username}';
                ''')
                no_str = cursor.fetchone()[0]
            
            #initiate form accordingly with fetched no_str and data from button click (table's row)
            form = form_update_appointment(initial=data)

        context = {'form': form}
        return render(request, "updateappointment.html", context)
    else:
        return render(request, 'home.html')

def deleteAppointment(request):
    if 'username' in request.session and (request.session['peran'] == 'ADMIN_SATGAS'):
        if request.method == 'GET':
            nik_pasien = request.GET.get('nik_pasien')
            username = request.GET.get('username')
            kode_faskes = request.GET.get('kode_faskes')
            shift = request.GET.get('shift')
            tanggal = request.GET.get('tanggal') 

            with connection.cursor() as cursor:
                cursor.execute(f'''
                select nostr from dokter
                where username = '{username}';
                ''')
                no_str = cursor.fetchone()[0]

            with connection.cursor() as cursor:
                cursor.execute(f'''
                delete from memeriksa where
                nik_pasien = '{nik_pasien}' and
                username_dokter = '{username}' and
                nostr = '{no_str}' and
                kode_faskes = '{kode_faskes}' and
                praktek_shift = '{shift}' and
                praktek_tgl = '{tanggal}';
                '''
                )
        return HttpResponseRedirect(reverse('memeriksa:list_appointment'))
    else:
        return render(request, 'home.html')