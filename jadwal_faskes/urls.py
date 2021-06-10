from django.urls import path
from .views import create_jadwal_faskes_view, list_jadwal_view

urlpatterns = [
    path('create/', create_jadwal_faskes_view, name='create_jadwal'),
    path('', list_jadwal_view, name='list_jadwal')
]