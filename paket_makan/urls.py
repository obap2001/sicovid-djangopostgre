from transaksi_makan.views import update_transaksi_makan_view
from django.urls import path
from .views import create_paket_makan_view, delete_paket_makan_view, list_paket_makan_view, update_paket_makan_view

urlpatterns = [
    path('', list_paket_makan_view, name='list_paket_makan'),
    path('create/', create_paket_makan_view, name='create_paket_makan'),
    path('delete/<str:kodeHotel>/<str:kodePaket>/', delete_paket_makan_view, name='delete_paket_makan'),
    path('update/<str:kodeHotel>/<str:kodePaket>/', update_paket_makan_view, name='update_paket_makan')

]