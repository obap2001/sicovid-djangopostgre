from django.urls import path
from .views import create_transaksi_makan_view, detail_transaksi_makan_view, fetch_data_transmakan, list_transaksi_makan_view, delete_transaksi_makan_view

urlpatterns = [
    path('create/', create_transaksi_makan_view, name='create_transaksi_makan'),
    path('', list_transaksi_makan_view, name='list_transaksi_makan'),
    path('create/load_kode_hotel', fetch_data_transmakan, name='kode_hotel_terpilih'),
    path('delete/<str:idtransaksimakan>', delete_transaksi_makan_view, name='delete_transmakan'),
    path('detail/<str:idtransaksi>/<str:idtransaksimakan>', detail_transaksi_makan_view, name='detail_transaksi_makan')
]