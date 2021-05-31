from django.http import response
from django.contrib import messages
from django.shortcuts import render
from django.db import connection, InternalError
from .forms import adminRegisterForm, penggunaPublikRegisterForm

# Register Admin
def registerAdmin(request):
    # response for Passing data into Templates
    response = {}

    # Institiate The Form
    form = adminRegisterForm(request.POST)

    # Assigning data for response
    response['form'] = form

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
                    ('{email}','{password}' ,'Admin Sistem');
                    insert into admin values
                    ('{email}');'''
                    )
                messages.success(request,f'Successfully Registerd, Welcome {email}')

            except InternalError:
                # Check if user already regitstered or not
                cursor.execute(
                    f'''set search_path to siruco;
                    SELECT USERNAME FROM AKUN_PENGGUNA
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
    return render(request, 'register.html',response)
