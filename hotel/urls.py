from django.urls import path
from .views import create_hotel_view

urlpatterns = [
    path('create/', create_hotel_view, name='create_hotel')

]