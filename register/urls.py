from django.urls import path
from .views import registerAdminSistem, registerPenggunaPublik, registerAdminSatgas, registerDokter

urlpatterns = [
    path('admin_sistem/', registerAdminSistem, name='register_admin_sistem'),
    path('pengguna_publik/', registerPenggunaPublik, name='register_pengguna_publik'),
    path('admin_satgas/', registerAdminSatgas, name='register_admin_satgas'),
    path('dokter/',registerDokter, name='register_dokter')
]