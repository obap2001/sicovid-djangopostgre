from django.urls import path
from .views import create_hotel_view, list_hotel_view, update_hotel_view

urlpatterns = [
    path('', list_hotel_view, name='list_hotel'),
    path('create/', create_hotel_view, name='create_hotel'),
    path('update/<str:kode>', update_hotel_view, name='update_hotel')

]