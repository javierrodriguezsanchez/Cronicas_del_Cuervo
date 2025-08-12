from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('ejemplo',views.VistaEjemplo,name='ejemplo'),
    #Foros 
    path('foro/', views.Foros_views.listado_hilos, name='listado_hilos'),
    path('hilo/nuevo/', views.Foros_views.crear_hilo, name='crear_hilo'),
    path('hilo/<int:pk>/', views.Foros_views.detalle_hilo, name='detalle_hilo'),
    path('hilo/<int:pk>/responder/', views.Foros_views.responder_hilo, name='responder_hilo'),
    path('buscar/', views.Foros_views.buscar_hilos, name='buscar_hilos'),
    #Autentificaciones
    path("registro/", views.Registro_views.registro_view, name="registro"),
    path('login/', auth_views.LoginView.as_view(template_name='Auths/Login_temp.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

