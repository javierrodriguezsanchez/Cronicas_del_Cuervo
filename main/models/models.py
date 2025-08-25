from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noticias')
    categoria = models.CharField(max_length=100)
    usuarios_like = models.ManyToManyField(User, related_name='noticias_like', blank=True)
    usuarios_dislike = models.ManyToManyField(User, related_name='noticias_dislike', blank=True)

    @property
    def likes(self):
        return self.usuarios_like.count()

    @property
    def dislikes(self):
        return self.usuarios_dislike.count()

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios')
    contenido = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    comentario_padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='respuestas')
    usuarios_like = models.ManyToManyField(User, related_name='comentarios_like', blank=True)

    @property
    def likes(self):
        return self.usuarios_like.count()

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.noticia.titulo[:20]}"
