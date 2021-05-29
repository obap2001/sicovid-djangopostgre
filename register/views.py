from django.http import response
from django.shortcuts import render
from django.db import connection
from .forms import adminRegisterForm, penggunaPublikRegisterForm

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

def registerPenggunaPublik(request):
    response = {}
    form = penggunaPublikRegisterForm(request.POST)
    response['form'] = form
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        nik = form.cleaned_data['nik']
        nama = form.cleaned_data['nama']
        status = form.cleaned_data['status']
        noHP = form.cleaned_data['noHP']

        # Execute Querry
        with connection.cursor() as cursor:
            cursor.execute(
                f'''insert into siruco.pengguna_publik values
                    ('{username}', '{nik}', '{nama}', '{status}', 'PENGGUNA PUBLIK', '{noHP}');
                '''
            )
    re
