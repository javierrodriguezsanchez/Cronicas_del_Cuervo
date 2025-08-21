from django.urls import include, path
from . import views
from django.contrib import admin

urlpatterns = [
    path('ejemplo',views.VistaEjemplo,name='ejemplo'),
    path("admin", views.admin_dashboard, name="admin_dashboard"),
]
