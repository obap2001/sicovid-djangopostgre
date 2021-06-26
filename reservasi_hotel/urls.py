from django.urls import path
from .views import create_reservasi_hotel_view, list_reservasi_hotel_view, update_reservasi_hotel_view, delete_reservasi_hotel_view, fetch_data_ruangan

urlpatterns = [
    path('create/',create_reservasi_hotel_view, name='create_ruangan_hotel'),
    path('',list_reservasi_hotel_view, name='list_ruangan_hotel'),
    path('update/<str:kode_pasien>/<str:tanggal>',update_reservasi_hotel_view, name='update_reservasi_hotel'),
    path('delete/<str:kode_pasien>/<str:tanggal>',delete_reservasi_hotel_view, name='delete_reservasi_hotel'),
    path('create/load_ruangan/',fetch_data_ruangan, name='load_ruangan'),

]