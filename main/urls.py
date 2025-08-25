from django.urls import path
from .views.comentarios_noticias import (
    comentarios_noticias,
    agregar_comentario,
    manejar_reaccion,
)  # Importación correcta de las vistas locales

urlpatterns = [
    path('comentarios/', comentarios_noticias, name='comentarios'),
    path('comentarios/agregar/', agregar_comentario, name='agregar_comentario'),
    path('comentarios/reaccion/', manejar_reaccion, name='manejar_reaccion'),
]