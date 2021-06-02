from django.db import connection
from django.shortcuts import redirect, render
from .forms import CreatePasienForm, CreatePasienDomisiliAlamatForm, CreatePasienKTPAlamatForm

# Create your views here.
def create_daftar_pasien_view(request):
    if 'username' in request.session and request.session['peran'] == 'PENGGUNA_PUBLIK':
        response = {}

        form_umum = CreatePasienForm(request.POST)
        form_KTP = CreatePasienKTPAlamatForm(request.POST)
        form_domisili = CreatePasienDomisiliAlamatForm(request.POST)

        response['form_umum'] = form_umum
        response['form_KTP'] = form_KTP
        response['form_domisili'] = form_domisili

        if request.method == 'POST' and form_umum.is_valid() and form_KTP.is_valid() and form_domisili.is_valid():
            nik = form_umum.cleaned_data['nik']
            nama = form_umum.cleaned_data['nama']
            nomor_telepon = form_umum.cleaned_data['nomor_telepon']
            nomor_hp = form_umum.cleaned_data['nomor_hp']

            jalan_ktp = form_KTP.cleaned_data['jalan']
            kelurahan_ktp = form_KTP.cleaned_data['kelurahan']
            kecamatan_ktp = form_KTP.cleaned_data['kecamatan']
            kabupaten_kota_ktp = form_KTP.cleaned_data['kabupaten_kota']
            provinsi_ktp = form_KTP.cleaned_data['provinsi']

            jalan_domisili = form_domisili.cleaned_data['jalan']
            kelurahan_domisili = form_domisili.cleaned_data['kelurahan']
            kecamatan_domisili = form_domisili.cleaned_data['kecamatan']
            kabupaten_kota_domisili = form_domisili.cleaned_data['kabupaten_kota']
            provinsi_domisili = form_domisili.cleaned_data['provinsi']

            with connection.cursor() as cursor:
                cursor.execute(
                    f'''insert into pasien values
                    ('{nik}','{request.session['username']}','{nama}','{jalan_ktp}','{kelurahan_ktp}','{kecamatan_ktp}','{kabupaten_kota_ktp}',
                    '{provinsi_ktp}','{jalan_domisili}','{kelurahan_domisili}','{kecamatan_domisili}',
                    '{kabupaten_kota_domisili}','{provinsi_domisili}, ,'{nomor_telepon}','{nomor_hp}')
                    '''
                )

        return render(request,'create_pasien.html',response)
    else:
        return redirect('home')