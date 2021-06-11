from django.http import response
from django.contrib import messages
from django.shortcuts import redirect, render
from django.db import connection, InternalError
from .forms import adminSistemRegisterForm, penggunaPublikRegisterForm, adminDokterRegisterForm,adminSatgasRegisterForm
from login.views import login

# Register Admin
def registerAdminSistem(request):
    # response for Passing data into Templates
    response = {}

    # Institiate The Form
    form = adminSistemRegisterForm(request.POST)

    # Assigning data for response
    response['form'] = form
    response['title'] = 'Register Admin Sistem'

    # Getting data from Form on POST
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        # Execute Query for Registering
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    f'''set search_path to siruco;
                    insert into akun_pengguna values
                    ('{email}','{password}' ,'ADMIN_SISTEM');
                    insert into admin values
                    ('{email}');'''
                    )
                messages.success(request,'Successfully Registered as Admin Sistem')
                login(request,email,password)
                return redirect('home')

            except InternalError:
                # Check if user already regitstered or not
                cursor.execute(
                    f'''set search_path to siruco;
                    SELECT USERNAME,PERAN FROM AKUN_PENGGUNA
                    WHERE USERNAME='{email}';'''
                    )
                data = cursor.fetchone()
                if data: # Exception if user already register
                    messages.error(request,'User has already been registered')
                else: # Exception if password does not match requirement
                    messages.error(request,'Password must have at least 1 capital letters and 1 number')

    return render(request,'register.html',response)

def registerPenggunaPublik(request):
    response = {}
    form = penggunaPublikRegisterForm(request.POST)
    response['form'] = form
    response['title'] = 'Register Pengguna Publik'
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        nama = form.cleaned_data['nama']
        nik = form.cleaned_data['nik']
        noHP = form.cleaned_data['noHP']

        # Execute Querry
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    f'''
                    insert into siruco.akun_pengguna values
                    ('{email}','{password}' ,'PENGGUNA_PUBLIK');
                    insert into siruco.pengguna_publik values
                    ('{email}', '{nik}', '{nama}', 'AKTIF', 'PENGGUNA_PUBLIK', '{noHP}');
                    '''
                )
                messages.success(request,'Successfully Registered as Pengguna Publik')
                login(request,email,password)
                return redirect('home')

            except InternalError:
                # Check if user already regitstered or not
                cursor.execute(
                    f'''set search_path to siruco;
                    SELECT USERNAME,PERAN FROM AKUN_PENGGUNA
                    WHERE USERNAME='{email}';'''
                    )
                data = cursor.fetchone()
                if data: # Exception if user already register
                    messages.error(request,'User has already been registered')
                else: # Exception if password does not match requirement
                    messages.error(request,'Password must have at least 1 capital letters and 1 number')

    return render(request, 'register.html',response)

def registerAdminSatgas(request):
    response = {}
    form = adminSatgasRegisterForm(request.POST)
    response['form'] = form
    response['title'] = 'Register Admin Satgas'
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        kode_faskes = form.cleaned_data['kode_faskes'] # Will get the kode_fakses instead of the name

        # Execute Query
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    f'''set search_path to siruco; 
                    insert into akun_pengguna values
                    ('{email}','{password}' ,'ADMIN_SATGAS');
                    insert into admin values ('{email}');
                    insert into admin_satgas values
                    ('{email}', '{kode_faskes}');'''
                    )
                messages.success(request,'Successfully Registered as Admin Satgas')
                login(request,email,password)
                return redirect('home')


            except InternalError:
                # Check if user already regitstered or not
                cursor.execute(
                    f'''set search_path to siruco;
                    SELECT USERNAME,PERAN FROM AKUN_PENGGUNA
                    WHERE USERNAME='{email}';'''
                    )
                data = cursor.fetchone()
                if data: # Exception if user already register
                    messages.error(request,'User has already been registered')
                else: # Exception if password does not match requirement
                    messages.error(request,'Password must have at least 1 capital letters and 1 number')

    return render(request,'register.html',response)

def registerDokter(request):
    response = {}
    form = adminDokterRegisterForm(request.POST)
    response['form'] = form
    response['title'] = 'Register Dokter'
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['username']
        password = form.cleaned_data['password']
        noSTR = form.cleaned_data['noSTR']
        nama = form.cleaned_data['nama']
        noHP = form.cleaned_data['noHP']
        gelarDepan = form.cleaned_data['gelarDepan']
        gelarBelakang = form.cleaned_data['gelarBelakang']

        # Execute Query
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    f'''set search_path to siruco; 
                    insert into akun_pengguna values
                    ('{email}','{password}' ,'DOKTER');
                    insert into admin values ('{email}');
                    insert into dokter values
                    ('{email}','{noSTR}','{nama}','{noHP}','{gelarDepan}','{gelarBelakang}');'''
                    )
                login(request,email,password)
                return redirect('home')

            except InternalError:
                # Check if user already regitstered or not
                cursor.execute(
                    f'''set search_path to siruco;
                    SELECT USERNAME,PERAN FROM AKUN_PENGGUNA
                    WHERE USERNAME='{email}';'''
                    )
                data = cursor.fetchone()
                if data: # Exception if user already register
                    messages.error(request,'User has already been registered')
                else: # Exception if password does not match requirement
                    messages.error(request,'Password must have at least 1 capital letters and 1 number')

    return render(request,'register.html',response)