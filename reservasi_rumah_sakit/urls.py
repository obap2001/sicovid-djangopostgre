from django.urls import path
from .views import create_reservasi_rs_view, delete_reservasi_rs_view, list_reservasi_rs_view, update_reservasi_rs_view
from .views import fetch_data_ruangan, fetch_data_bed

urlpatterns = [
    path('create/',create_reservasi_rs_view, name='create_reservasi_rs'),
    path('delete/<str:kode_pasien>/<str:tanggal>',delete_reservasi_rs_view, name='delete_reservasi_rs'),
    path('update/<str:kode_pasien>/<str:tanggal>',update_reservasi_rs_view, name='update_reservasi_rs'),
    path('',list_reservasi_rs_view, name='list_reservasi_rs'),
    path('create/load_ruangan/',fetch_data_ruangan, name='load_ruangan'),
    path('create/load_bed/',fetch_data_bed, name='load_bed'),
]