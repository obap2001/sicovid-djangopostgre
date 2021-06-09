from django.urls import path
from .views import create_faskes_view, list_faskes_view

urlpatterns = [
    path('create/', create_faskes_view, name='create_pasien'),
    path('', list_faskes_view, name='list_faskes')
]