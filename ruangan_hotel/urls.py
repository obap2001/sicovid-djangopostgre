from django.urls import path
from .views import create_ruangan_hotel_view, list_ruangan_hotel_view, update_ruangan_hotel_view, delete_ruangan_hotel_view

urlpatterns = [
    path('create/',create_ruangan_hotel_view, name='create_ruangan_hotel'),
    path('',list_ruangan_hotel_view, name='list_ruangan_hotel'),
    path('update/<str:kode_hotel>/<str:kode_ruangan>',update_ruangan_hotel_view, name='update_ruangan_hotel'),
    path('delete/<str:kode_hotel>/<str:kode_ruangan>',delete_ruangan_hotel_view, name='delete_ruangan_hotel')
]