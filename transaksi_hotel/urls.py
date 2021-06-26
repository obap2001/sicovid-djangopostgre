from django.urls import path
from .views import list_transaksi_hotel_view, delete_transaksi_hotel_view, update_transaksi_hotel_view

urlpatterns = [
    path('',list_transaksi_hotel_view, name='list_transaksi_hotel'),
    # path('delete/<str:id>/',delete_transaksi_hotel_view, name='delete_transaksi_hotel'),
    path('update/<str:id>/',update_transaksi_hotel_view, name='update_transaksi_hotel')
]