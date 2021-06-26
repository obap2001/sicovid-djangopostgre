from django.http import response
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.db import connection, InternalError
from datetime import datetime 
from .forms import *

#Create your views here.

def createBedRS(request):
    if 'username' in request.session and (request.session['peran'] == 'ADMIN_SATGAS'):
        form = form_create_bedrs()

        rumahsakit = [] #init koders
        ruangan = [] #init ruangan

        with connection.cursor() as cursor:
            cursor.execute(f'''
            select kode_faskes from rumah_sakit;
            ''')
            rumahsakit = cursor.fetchall()
        
        with connection.cursor() as cursor:
            cursor.execute(f'''
            select kode_faskes from rumah_sakit;
            ''')
            rumahsakit = cursor.fetchall()

        if request.method == 'POST':
            kode_rs = request.POST['kode_rs']
            kode_ruangan = request.POST['ruangan_rs']
            kode_bed = request.POST['bed_rs']

            data_baru = [kode_ruangan, kode_rs, kode_bed]
            print(data_baru)
            with connection.cursor() as cursor:
                cursor.execute(f'''
                insert into bed_rs values(
                    '{kode_ruangan}', '{kode_rs}', '{kode_bed}')''')
                return redirect('ruangan_bed_rs:list_bedrs')
        context = {'form':form}
        
        return render(request, 'createbedrs.html', context)

    else:
        return render(request, 'home.html')

def listBedRS(request):
    if 'username' in request.session and (request.session['peran'] == 'ADMIN_SATGAS'):
        context = {} #init response
        data_bed = [] #init data
        with connection.cursor() as cursor:
            cursor.execute(f'''
            select * from bed_rs;
            ''')
            data_bed = cursor.fetchall()
        context['data_bed']= data_bed
        return render(request, "listbedrs.html", context)
    else:
        return render(request, 'home.html')

def deleteBedRS(request):
    if 'username' in request.session and (request.session['peran'] == 'ADMIN_SATGAS'):
        return render(request, "deletebedrs.html")
    else:
        return render(request, 'home.html')

def createRuanganRS(request):
    if 'username' in request.session and (request.session['peran'] == 'ADMIN_SATGAS'):
        form = form_create_ruanganrs()
        
        with connection.cursor() as cursor:
            cursor.execute(f'''
            select kode_faskes from rumah_sakit;
            ''')
            allcode = cursor.fetchall()

        if request.method == 'POST':
            kode_rs = request.POST['kode_rs']
            kode_ruangan = request.POST['kode_ruangan']
            jml_bed = 0
            harga_ruangan = request.POST['harga_ruangan']
            tipe = request.POST['tipe']

            with connection.cursor() as cursor:
                cursor.execute(f'''
                    insert into ruangan_rs values(
                    '{kode_rs}', '{kode_ruangan}', '{tipe}', '{jml_bed}', '{harga_ruangan}')
                    ''')
            return redirect('ruangan_bed_rs:list_ruanganrs')

        return render(request, 'createruanganrs.html', {'form': form, 'kode_rs':allcode})
    else:
        return render(request, 'home.html')

def listRuanganRS(request):
    if 'username' in request.session and (request.session['peran'] == 'ADMIN_SATGAS'):
        context = {}
        data_ruangan_rs = []
        with connection.cursor() as cursor:
            cursor.execute(f'''
            select * 
            from ruangan_rs''')
            data_ruangan_rs = cursor.fetchall()
            
        context['data_ruangan_rs'] = data_ruangan_rs
        return render(request, "listruanganrs.html", context)
    else:
        return render(request, 'home.html')

def updateRuanganRS(request):
    if 'username' in request.session and (request.session['peran'] == 'ADMIN_SATGAS'):
        if request.method == 'POST': #on post: when button 'simpan' is clicked
            kode_rs = request.POST['kode_rs']
            kode_ruangan = request.POST['kode_ruangan']
            harga = request.POST['harga']
            tipe = request.POST['tipe']

            with connection.cursor() as cursor:
                cursor.execute(f'''
                update ruangan_rs
                set tipe = '{tipe}',
                harga = '{harga}' 
                where koders = '{kode_rs}' and
                koderuangan = '{kode_ruangan}';
                ''')
            return redirect('ruangan_bed_rs:list_ruanganrs')

        elif request.method == 'GET': #on get: when button 'update' is clicked
            kode_rs = request.GET.get('kode_rs')
            kode_ruangan = request.GET.get('kode_ruangan')

            data_for_form = {
                'kode_rs': kode_rs,
                'kode_ruangan': kode_ruangan
            }

            form = form_update_ruanganrs(initial=data_for_form)
        context = {'form':form}
        return render(request, 'updateruanganrs.html', context)
    else:
        return render(request, 'home.html')

def ajaxRuanganRS(request, a):
    kode_rs = a
    with connection.cursor() as cursor:
        cursor.execute(f'''
        select koderuangan from ruangan_rs
        where koders = '{kode_rs}'
        order by koderuangan desc
        limit 1;
        ''')

        try:
            initial_code = cursor.fetchone()[0]
            print("initial code =" + initial_code)
            updated_code = str(int(initial_code) + 1)
            print("updated code=" + updated_code)
        except:
            updated_code = "R1" + kode_rs
    return JsonResponse({'id':updated_code})


# UNFINISHED
def ajaxBedRS(request, b):
    kode_ruangan = b
    with connection.cursor() as cursor:
        cursor.execute(f'''
        select kodebed from bed_rs
        where koderuangan = '{kode_ruangan}'
        order by kodebed desc
        limit 1;
        ''')
        try:
            initialcode = cursor.fetchone()[0]
            print("initial code =" + initialcode)
            updatedcode = str(int(initialcode) + 1)
            print("updated code=" + updatedcode)
        except:
            updatedcode = "B1" + kode_ruangan
    return JsonResponse({'id':updatedcode})