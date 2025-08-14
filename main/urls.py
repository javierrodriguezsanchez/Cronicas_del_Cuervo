from django.urls import path
from . import views

urlpatterns = [
    path('ejemplo', views.VistaEjemplo, name='ejemplo'),

    # Admin-only CRUD for journals
    path('journals/', views.admin_journals, name='admin_journals'),
    path('journals/<int:pk>/edit/', views.edit_journal, name='edit_journal'),
    path('journals/<int:pk>/delete/', views.delete_journal, name='delete_journal'),
    path('admin/noticias-a-word/', views.export_news_to_word, name='export_news_to_word'),

    # Public download page & file
    path('descargar-diario/', views.public_journal_page, name='public_journal_page'),
    path('descargar-diario/<int:pk>/', views.download_journal_file, name='download_journal_file'),
]
