from django.urls import path
from . import views


urlpatterns = [
    path('ejemplo',views.VistaEjemplo,name='ejemplo'),
    path('admin',views.VistaAdmin,name='admin')
]