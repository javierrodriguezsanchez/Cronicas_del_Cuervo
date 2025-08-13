from django.db import models 
from django.contrib.auth.models import User
from django import forms



class Hilo(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    cerrado = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag', blank=True, related_name='hilos')
    

    @property
    def ultima_respuesta(self):
        if self.respuestas.exists():
            return self.respuestas.latest('fecha_creacion').fecha_creacion
        return self.fecha_creacion