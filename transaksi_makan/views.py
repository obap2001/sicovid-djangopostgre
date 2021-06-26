from django.http import response
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import close_old_connections, connection
from .forms import UpdatePesananForm, UpdateTransaksiForm, createTransaksiMakanForm, fetch_data_transaksi_hotel, pesananForm
from .forms import DetailTransaksiMakanForm, DetailPesananForm

# Create your views here.
def create_transaksi_makan_view(request):
    if ('username' in request.session and request.session['peran'] == 'PENGGUNA_PUBLIK') or ('username' in request.session and request.session['peran'] == 'ADMIN_SATGAS') :
        response = {}

        # Count ID
        id_all = []
        with connection.cursor() as cursor:
            cursor.execute('SELECT idTransaksiMakan FROM transaksi_makan;')
            id_all = cursor.fetchall()

        # Cleaned data
        data_clean = []
        for i in id_all:
            data_clean.append(i[0])

        # Generate all possible id
        id_now = ''
        for i in range(1,1000):
            if i < 10 :
                id_now = 'TRM00' + str(i)
            elif i <100 :
                id_now = 'TRM0' + str(i)
            else:
                id_now = 'TRM' + str(i)

            if id_now not in data_clean:
                break
        
        # Count ID_pesanan
        id_allp = []
        with connection.cursor() as cursor:
            cursor.execute('SELECT id_pesanan FROM daftar_pesan;')
            id_allp = cursor.fetchall()

        # Cleaned data
        data_cleanp = []
        for i in id_allp:
            data_cleanp.append(i[0])

        # Generate all possible id
        id_nowp = 1
        for i in data_cleanp:
            if id_nowp != i:
                break
            else:
                id_nowp += 1        

        #instantiate form
        initial_data = {'id_transaksi_makan' : id_now}
        form_transmakan = createTransaksiMakanForm(request.POST or None, initial=initial_data)
        form_pesanan = pesananForm(request.POST or None)

        #passing form to response
        response['form_transmakan'] = form_transmakan
        response['form_pesanan'] = form_pesanan

        

        #validate form
        if request.method == 'POST' and form_transmakan.is_valid():
            id_transaksi = form_transmakan.cleaned_data['id_transaksi']
            id_transaksi_makan = form_transmakan.cleaned_data['id_transaksi_makan']
            kode_hotel = form_transmakan.cleaned_data['kode_hotel']
            kode_paket = form_pesanan.cleaned_data['kode_paket']

            #Count totalharga of paket makanan masih perlu diperbaiki (case paket >1)
            list_harga = []
            with connection.cursor() as cursor:
                cursor.execute(f'''
                    SELECT harga FROM paket_Makan
                    WHERE kodeHotel = '{kode_hotel}' AND kodePaket = '{kode_paket}';
                ''')
                list_harga = cursor.fetchall()

            #Insert data on table
            with connection.cursor() as cursor:
                cursor.execute(f'''
                INSERT INTO transaksi_makan values (
                    '{id_transaksi}','{id_transaksi_makan}'
                );
                INSERT into daftar_pesan values (
                    '{id_transaksi_makan}', {id_nowp}, '{id_transaksi}', '{kode_hotel}', '{kode_paket}'
                );
                ''')
            messages.success(request, f'Transaksi Makana Berhasil ditambahkan')
            return redirect('daftar_transaksi_makan')

        # elif request.method == 'GET':
        #     kode_hotel = request.GET.get('')

        return render(request, 'create_transmakan.html', response)

    else:
        return redirect('home')

def list_transaksi_makan_view(request):
    if ('username' in request.session and request.session['peran'] == 'PENGGUNA_PUBLIK') or ('username' in request.session and request.session['peran'] == 'ADMIN_SATGAS') :
        response = {}
        deletable_data_transMakan = []
        undeletable_data_transMakan = []

        #fetch data transaksi makan
        with connection.cursor() as cursor:
            cursor.execute(f'''
                  SELECT idtransaksi, idtransaksimakan, totalbayar
                  FROM transaksi_makan
                  WHERE idtransaksi NOT IN (
                      SELECT idtransaksi from transaksi_hotel
                      WHERE statusbayar = 'Lunas'
                  );
            ''')
            deletable_data_transMakan = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(f'''
                  SELECT idtransaksi, idtransaksimakan, totalbayar
                  FROM transaksi_makan
                  WHERE idtransaksi IN (
                      SELECT idtransaksi from transaksi_hotel
                      WHERE statusbayar = 'Lunas'
                  );
            ''')
            undeletable_data_transMakan = cursor.fetchall()

        data_gabung = []
        for i in deletable_data_transMakan:
            temp = (f'{i[0]}', f'{i[1]}', f'{i[2]}', True)
            data_gabung.append(temp)

        for i in undeletable_data_transMakan:
            temp = (f'{i[0]}', f'{i[1]}', f'{i[2]}', False)
            data_gabung.append(temp)

        data_gabung.sort()
        cleaned_data = []
        angka = 1
        for i in data_gabung:
            temp = (f'{i[0]}', f'{i[1]}', f'{i[2]}', f'{i[3]}', angka)
            cleaned_data.append(temp)
            angka+=1

        response['data_transmakan'] = cleaned_data
        return render(request, 'list_transmakan.html', response)
    else:
        return redirect('home')


def detail_transaksi_makan_view(request, idtransaksi, idtransaksimakan):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SATGAS' :
        response = {}
        kode_hotel = []
        total_bayar = []
        with connection.cursor() as cursor:
            cursor.execute(f'''
                SELECT kodehotel from daftar_pesan
                WHERE id_transaksi='{idtransaksi}' and idtransaksimakan = '{idtransaksimakan}';
            ''')
            kode_hotel = cursor.fetchone()
            cursor.execute(f'''
                SELECT totalBayar from transaksi_makan
                WHERE idtransaksi = '{idtransaksi}' and idtransaksimakan = '{idtransaksimakan}';
            ''')
            total_bayar = cursor.fetchone()
        if not kode_hotel:
            return False

        data_pesanan = []
        with connection.cursor() as cursor:
            cursor.execute(f'''
                SELECT DP.id_pesanan, DP.kodepaket, PM.harga 
                from daftar_pesan DP JOIN paket_makan PM ON (DP.kodepaket=PM.kodepaket and DP.kodeHotel = PM.kodeHotel)
                WHERE dp.idtransaksimakan = '{idtransaksimakan}' and dp.id_transaksi = '{idtransaksi}';
            ''')
            data_pesanan = cursor.fetchall()
        if not data_pesanan:
            return False

        init_kode_hotel = {
            'idtransaksi' : idtransaksi,
            'idtransaksimakan' : idtransaksimakan,
            'kodeHotel' : kode_hotel[0]
        }
        init_data_pesan = {
            'id_pesanan' : data_pesanan[0],
            'kodepaket' : data_pesanan[1],
            'harga' : data_pesanan[2]
        }
        #Instantiate Form
        form_transaksi = DetailTransaksiMakanForm(request.POST or None, initial=init_kode_hotel)
        form_pesanan = DetailPesananForm(request.POST or None, initial=init_data_pesan)

        data_all = []
        data_pesan = []
        data_all.append(idtransaksi)
        data_all.append(idtransaksimakan)
        for i in kode_hotel:
            data_all.append(kode_hotel[0])

        for i in data_pesanan:
            temp = [f'{i[0]}', f'{i[1]}', f'{i[2]}']
            data_pesan.append(temp)
        data_all.append(total_bayar[0])

        #Passing form to response
        response['data_all'] = data_all
        response['data_pesanan'] = data_pesan

        return render(request, 'detail_transmakan.html', response)

    else:
        return redirect('home')

def update_transaksi_makan_view(request, idtransaksimakan):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SATGAS':
        response = {}
        data_transmakan = fetch_data_transaksi_makan(idtransaksimakan)

        #fetch data transaksi makan
        if not data_transmakan:
            messages.error(request, 'Data Transaksi Makan Tidak Ditemukan')
            return redirect('home')

        #intantiate Form
        form_transmakan = UpdateTransaksiForm(request.POST or None, initial=data_transmakan[0])
        form_pesanan = UpdatePesananForm(request.POST or None, initial=data_transmakan[1])

        #Passing Form to Response
        response['form_transaksi'] = form_transmakan
        response['form_pesanan'] = form_pesanan

        #Form Validation
        if request.method == 'POST' and form_transmakan.is_valid() and form_pesanan.is_valid():
            idtransaksi = form_transmakan.cleaned_data['idtransaksi']
            idtransaksimakan = form_transmakan.cleaned_data['idtransaksimakan']


def fetch_data_transaksi_makan(request, idtransaksi, kode):
    data_transmakan = []
    with connection.cursor() as cursor:
        cursor.execute(f'''
           SELECT idtransaksi, idtransaksimakan FROM transaksi_makan
           WHERE idtransaksimakan='{kode}';
        ''')
        data_transmakan = cursor.fetchone()

    if not data_transmakan:
        return False

    kode_hotel = []
    with connection.cursor() as cursor:
        cursor.execute(f'''
             SELECT kodehotel from daftar_pesan
             WHERE id_transaksi='{idtransaksi}' and idtransaksimakan = '{kode}';
        ''')
        kode_hotel = cursor.fetchone()

    if not kode_hotel:
        return False

    data_pesanan = []
    with connection.cursor() as cursor:
        cursor.execute(f'''
             SELECT DP.id_pesanan, DP.kodepaket, PM.harga 
             from daftar_pesan DP JOIN paket_makan PM ON DP.kodepaket=PM.kodepaket
             WHERE dp.idtransaksimakan = '{kode}';
        ''')
        data_pesanan = cursor.fetchone()

    if not data_pesanan:
        return False

    init_transaksi_data ={
        'idtransaksi' : data_transmakan[0],
        'idtransaksimakan' : data_transmakan[1],
        'kodehotel' : kode_hotel[0]
    }

    init_pesanan_data = {
        'idpesanan' : data_pesanan[0],
        'kodepaket' : data_pesanan[1],
        'harga' : data_pesanan[2]
    }

    return [init_transaksi_data,init_pesanan_data]

def fetch_data_transmakan(request):
    tm = request.GET.get('idTransaksi')
    list_hotel = []

    with connection.cursor() as cursor:
        cursor.execute(f'''
             SELECT RH.kodeHotel
             FROM transaksi_hotel TH JOIN reservasi_hotel RH ON TH.kodepasien=RH.kodepasien
             WHERE TH.idtransaksi = '{tm}';
        ''')
        list_hotel = cursor.fetchone()

    #Organized the data
    cleaned_data = []
    for i in list_hotel:
        temp=(i[0],f'{i[0]}')
        cleaned_data.append(temp)
    return render(request, 'kode_hotel_chosen.html', {list_hotel : cleaned_data})

def delete_transaksi_makan_view(request, idtransaksimakan):
    if 'username' in request.session and request.session['peran'] == 'ADMIN_SATGAS':
        #Deleting data in SQL
        with connection.cursor() as cursor:
            cursor.execute(f'''
                  DELETE from transaksi_makan 
                  WHERE idtransaksimakan='{idtransaksimakan}' and idtransaksi in (
                      SELECT idtransaksi FROM transaksi_hotel
                      WHERE statusbayar = 'Belum Bayar');
            ''')
        # messages.success(request, f'Data Transaksi Makan Berhasil Dihapus')
        return redirect('list_transaksi_makan')

    else:
        # messages.error(request, 'Penghapusan Data Tidak Dapat Dilakukan')
        return redirect('home')