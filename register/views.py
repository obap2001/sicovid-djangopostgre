from django.http import response
from django.shortcuts import render
from django.db import connection
from .forms import adminRegisterForm

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