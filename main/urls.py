from django.urls import include, path
from . import views


urlpatterns = [
    path('ejemplo',views.VistaEjemplo,name='ejemplo'),
    path('admin',views.VistaAdmin,name='admin'),
    path("admin/", views.admin_dashboard, name="admin_dashboard"),
    path("", include("news.urls")),
]
