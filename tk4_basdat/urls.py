"""tk4_basdat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from base_html.views import home_view
from login.views import login_view, logout_view

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', include('register.urls')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('daftar_pasien/', include('pendaftaran_pasien.urls')),
    path('reservasi_rumah_sakit/', include('reservasi_rumah_sakit.urls')),
    path('faskes/', include('faskes.urls')),
    path('jadwal_faskes/', include('jadwal_faskes.urls')),
    path('rumah_sakit/',include('rumah_sakit.urls')),
    path('transaksi_rs/',include('transaksi_rumah_sakit.urls')),
    path('transaksi_makan/', include('transaksi_makan.urls')),
    path('paket_makan/', include('paket_makan.urls')),
    path('cr_jadwal_dokter/', include('cr_jadwal_dokter.urls')),
    path('hotel/', include('hotel.urls')),
    path('ruangan_hotel/',include('ruangan_hotel.urls')),
    path('transaksi_hotel/',include('transaksi_hotel.urls')),
    path('transaksi_booking/',include('transaksi_booking.urls')),
    path('reservasi_hotel/',include('reservasi_hotel.urls')),
    path('cr_jadwal_dokter/', include('cr_jadwal_dokter.urls')),
    path('memeriksa/', include('memeriksa.urls'))
]
