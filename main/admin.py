from django.contrib import admin
from .models import Noticia, Etiquetas, Categoría, Autor

@admin.register(Noticia)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ['título', 'fecha_de_publicación', 'categoría']
    list_filter = ['fecha_de_publicación', 'categoría']

admin.site.register(Etiquetas)
admin.site.register(Categoría)
admin.site.register(Autor)
