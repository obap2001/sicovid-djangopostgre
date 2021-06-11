from django.contrib import messages
from django.shortcuts import redirect, render
from django.db import connection
from .forms import loginForm

# Create your views here.
def login_view(request):
    if 'username' in request.session: # Check if user logged in or not
        return redirect('home')

    else:
        response = {}
        form = loginForm(request.POST or None)
        response['form'] = form
        response['title'] = 'Register Pengguna Publik'

        if request.method == 'POST' and form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            login(request,email,password)

        if 'username' in request.session:
            return redirect('home')
        else:
            return render(request,'login.html', response)

def login(request, username, password):
    data = None
    with connection.cursor() as cursor:
        cursor.execute(
            f'''set search_path to siruco;
            SELECT USERNAME,PERAN FROM AKUN_PENGGUNA
            WHERE USERNAME='{username}' AND PASSWORD='{password}';'''
            )
        data = cursor.fetchone()

    if data:
        request.session['username'] = data[0]
        request.session['peran'] = data[1]
        messages.success(request,f'Successfully logged in as {data[0]}')

def logout_view(request):
    request.session.flush()
    messages.success(request,'You have been logged out')
    return redirect('home')