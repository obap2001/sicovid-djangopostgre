from django.http import response
from django.shortcuts import render
from django.db import connection
from .forms import adminRegisterForm, adminSatgasRegisterForm,adminDokterRegisterForm

# Create your views here.
def registerAdmin(request):
    response = {}
    form = adminRegisterForm(request.POST)
    response['form'] = form
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        # Execute Query
        with connection.cursor() as cursor:
            cursor.execute(
                f'''set search_path to siruco; 
                insert into akun_pengguna values
                ('{email}','{password}' ,'Admin Sistem');
                insert into admin values
                ('{email}');'''
                )
    return render(request,'register.html',response)

def registerAdminSatgas(request):
    response = {}
    form = adminSatgasRegisterForm(request.POST)
    response['form'] = form
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        kode_faskes = form.cleaned_data['kode_faskes']
    
        # Execute Query
        with connection.cursor() as cursor:
            cursor.execute(
                f'''set search_path to siruco; 
                insert into akun_pengguna values
                ('{email}','{password}' ,'Admin Satgas');
                insert into admin_satgas values
                ('{email}', '{kode_faskes}');'''
                )
    return render(request,'register.html',response)

def registerDokter(request):
    response = {}
    form = adminDokterRegisterForm(request.POST)
    response['form'] = form
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        peran = form.cleaned_data['peran']
        nama = form.cleaned_data['nama']
        noHP = form.cleaned_data['noHP']
        gelarDepan = form.cleaned_data['gelarDepan']
        gelarBelakang = form.cleaned_data['gelarBelakang']

        # Execute Query
        with connection.cursor() as cursor:
            cursor.execute(
                f'''set search_path to siruco; 
                insert into akun_pengguna values
                ('{email}','{password}' ,'Admin Sistem');
                insert into admin values
                ('{email}');
                insert into dokter values
                ('{email}');'''
                )

    return render(request,'register.html',response)