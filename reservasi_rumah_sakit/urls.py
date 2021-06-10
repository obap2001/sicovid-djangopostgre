from django.urls import path
from .views import create_reservasi_rs_view, delete_reservasi_rs_view, detail_reservasi_rs_view, list_reservasi_rs_view, update_reservasi_rs_view
from .views import fetch_data_ruangan

urlpatterns = [
    path('create/',create_reservasi_rs_view, name='create_reservasi'),
    path('delete/<str:kode_pasien>/<str:tanggal>',delete_reservasi_rs_view, name='delete_reservasi'),
    path('detail/<str:kode_pasien>/<str:tanggal>',detail_reservasi_rs_view, name='detail_reservasi'),
    path('update/<str:kode_pasien>/<str:tanggal>',update_reservasi_rs_view, name='update_reservasi'),
    path('',list_reservasi_rs_view, name='list_reservasi'),
    path('create/load_ruangan',fetch_data_ruangan, name='load_ruangan')
]