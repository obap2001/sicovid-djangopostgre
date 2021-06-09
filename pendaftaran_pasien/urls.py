from django.urls import path
from .views import create_daftar_pasien_view, read_daftar_pasien_view, detail_daftar_pasien_view, delete_daftar_pasien_view, update_daftar_pasien_view

urlpatterns = [
    path('create/', create_daftar_pasien_view, name='create_pasien'),
    path('', read_daftar_pasien_view, name='daftar_pasien'),
    path('detail/<str:nik>',detail_daftar_pasien_view, name='detail_pasien'),
    path('update/<str:nik>',update_daftar_pasien_view, name='update_pasien'),
    path('delete/<str:nik>',delete_daftar_pasien_view, name='delete_pasien')
]