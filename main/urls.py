from django.urls import path
from . import views


urlpatterns = [
    path('ejemplo',views.VistaEjemplo,name='ejemplo'),
    path('Admin',views.VistaEjemplo,name='Admin')
]