from django.urls import path
from .views import *

app_name = 'ruangan_bed_rs'

urlpatterns = [
    path('create_ruanganrs/', createRuanganRS, name='create_ruanganrs'),
    path('list_ruanganrs/', listRuanganRS, name='list_ruanganrs'),
    path('update_ruanganrs/', updateRuanganRS, name='update_ruanganrs'),
    path('ajax_ruanganrs/<str:a>', ajaxRuanganRS, name='ajax_ruanganrs'),

    path('create_bedrs/', createBedRS, name='create_bedrs' ),
    path('list_bedrs/', listBedRS, name='list_bedrs' ),
    path('delete_bedrs/', deleteBedRS, name='delete_bedrs' ),
    path('ajax_bedrs/<str:b>', ajaxBedRS, name='ajax_bedrs' )
]