from django.urls import path
from .views import createJadwalDokter, listJadwalDokter, listJadwalDokterSendiri

app_name = 'cr_jadwal_dokter'

urlpatterns = [
    path('create_jadwal_dokter/', createJadwalDokter, name='create_jadwal_dokter'),
    path('list_jadwal_dokter_sendiri/', listJadwalDokterSendiri, name='list_jadwal_dokter_sendiri'),
    path('list_jadwal_dokter/', listJadwalDokter, name='list_jadwal_dokter')
]