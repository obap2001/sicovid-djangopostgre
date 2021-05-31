from django.urls import path
from .views import registerAdmin, registerPenggunaPublik

urlpatterns = [
    path('admin/', registerAdmin, name='register_admin'),
    path('penggunapublik/', registerPenggunaPublik, name='register_pengguna_publik')
]