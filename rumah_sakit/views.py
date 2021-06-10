from django.contrib import messages
from django.db import connection
from django.shortcuts import redirect, render
from .forms import CreateRSForm, UpdateRSForm

# Create your views here.
def create_rs_view(request):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SATGAS':
        response = {}

        #Instantiate Form
        form_rs = CreateRSForm(request.POST or None)

        #Passing form to response
        response['form_rs'] = form_rs

        #Validate Form
        if request.method == 'POST' and form_rs.is_valid():
            faskes = form_rs.cleaned_data['faskes']
            rujukan = form_rs.cleaned_data['rujukan']

            is_rujukan = None
            if rujukan:
                is_rujukan = 1
            else:
                is_rujukan = 0

            # Insert Data on table
            with connection.cursor() as cursor:
                cursor.execute(f'''
                INSERT INTO RUMAH_SAKIT values
                ('{faskes}','{is_rujukan}')
                ''')
            messages.success(request,f'RUMAH_SAKIT Berhasil Ditambahkan')
            return redirect('list_rs')

        return render(request,'create_rs.html',response)

    else:
        return render('home')

def list_rs_view(request):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SATGAS':
        response = {}
        data_rs = []

        # Fetch Data
        with connection.cursor() as cursor:
            cursor.execute(f'''
            SELECT * FROM RUMAH_SAKIT;
            ''')
            data_rs = cursor.fetchall()

        response['data_rs'] = data_rs
        return render(request,'list_rs.html',response)

    else:
        return render('home')

def update_rs_view(request,kode_faskes):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SATGAS':
        response = {}
        data_rs = []

        # Fetch Data RS
        with connection.cursor() as cursor:
            cursor.execute(
                f'''SELECT * FROM RUMAH_SAKIT where kode_faskes='{kode_faskes}' '''
            )
            data_rs = list(cursor.fetchone())

        if data_rs[1] == '0':
            data_rs[1] = False
        else:
            data_rs[1] = True

        #Intialized form
        init_rs_data = {
            'faskes' : data_rs[0],
            'rujukan' : data_rs[1]
        }

        # Instantiate Form
        form_rs = UpdateRSForm(request.POST or None, initial=init_rs_data)

        # Posting form to response
        response['form_rs'] = form_rs

        # Form Validation
        if request.method == 'POST' and form_rs.is_valid():
            faskes = form_rs.cleaned_data['faskes']
            rujukan = form_rs.cleaned_data['rujukan']

            is_rujukan = None
            if rujukan:
                is_rujukan = 1
            else:
                is_rujukan = 0

            with connection.cursor() as cursor:
                cursor.execute(f'''
                UPDATE RUMAH_SAKIT SET
                isrujukan = '{is_rujukan}'
                WHERE kode_faskes = '{faskes}';
                ''')

            messages.success(request,'Data Rumah sakit Berhasil diubah')
            return redirect('list_rs')

        return render(request, 'update_rs.html',response)

    else:
        return redirect('home')