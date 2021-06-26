from django.urls import path
from .views import list_transaksi_booking_view

urlpatterns = [
    path('',list_transaksi_booking_view, name='list_transaksi_booking'),
]