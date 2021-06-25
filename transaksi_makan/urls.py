from django.urls import path
from .views import create_transaksi_makan_view

urlpatterns = [
    path('', create_transaksi_makan_view, name='create_transaksi_makan')
]