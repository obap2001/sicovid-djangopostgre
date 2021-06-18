from django.urls import path
from .views import list_transaksi_rs_view, delete_transaksi_rs_view, update_transaksi_rs_view

urlpatterns = [
    path('delete/<str:id>/',delete_transaksi_rs_view, name='delete_transaksi_rs'),
    path('update/<str:id>/',update_transaksi_rs_view, name='update_transaksi_rs'),
    path('',list_transaksi_rs_view, name='list_transaksi_rs')
]