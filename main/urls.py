from django.urls import path
from . import views

urlpatterns = [
    path('ejemplo',views.VistaEjemplo,name='ejemplo'),
    path('foro/', views.Foros_views.listado_hilos, name='listado_hilos'),
    path('hilo/nuevo/', views.Foros_views.crear_hilo, name='crear_hilo'),
    path('hilo/<int:pk>/', views.Foros_views.detalle_hilo, name='detalle_hilo'),
    path('buscar/', views.Foros_views.buscar_hilos, name='buscar_hilos'),
]

