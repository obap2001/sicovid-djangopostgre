from django.urls import path
from .views import create_rs_view, update_rs_view, list_rs_view

urlpatterns = [
    path('create/', create_rs_view, name='create_rs'),
    path('', list_rs_view, name='list_rs'),
    path('update/<str:kode_faskes>',update_rs_view, name='update_rs')
]