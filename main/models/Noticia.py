from django.db import models
from .autor import Autor
from .Etiquetas import Etiquetas
from .Categoria import Categoría

class Noticia(models.Model):
    título = models.CharField(max_length=255)
    contenido = models.TextField()
    autores = models.ManyToManyField(Autor, related_name='articles')
    etiquetas = models.ManyToManyField(Etiquetas, related_name='all_news')
    categoría = models.ForeignKey(Categoría, on_delete=models.PROTECT, related_name='articles')
    fecha_de_publicación = models.DateField()

    def __str__(self):
        return self.título
