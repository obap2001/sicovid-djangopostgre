from django.urls import path
from .views import *

app_name = 'memeriksa'

urlpatterns = [
    path('create_appointment/', createAppointment, name='create_appointment'),
    path('list_appointment/', listAppointment, name='list_appointment'),
    path('form_appointment/', formAppointment, name='form_appointment'),
    path('update_appointment/', updateAppointment, name='update_appointment'),
    path('delete_appointment/', deleteAppointment, name='delete_appointment')
]