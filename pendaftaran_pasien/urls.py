from django.urls import path
from .views import create_daftar_pasien_view

urlpatterns = [
    path('create/', create_daftar_pasien_view, name='create_daftar_pasien'),
]