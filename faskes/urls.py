from django.urls import path
from .views import create_faskes_view, list_faskes_view, detail_faskes_view, update_faskes_view, delete_faskes_view

urlpatterns = [
    path('create/', create_faskes_view, name='create_faskes'),
    path('', list_faskes_view, name='list_faskes'),
    path('detail/<str:kode>', detail_faskes_view, name='detail_faskes'),
    path('update/<str:kode>', update_faskes_view, name='update_faskes'),
    path('delete/<str:kode>', delete_faskes_view, name='delete_faskes')
]