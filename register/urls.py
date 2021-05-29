from django.urls import path
from .views import registerAdmin

urlpatterns = [
    path('admin/', registerAdmin, name='register_admin')
]