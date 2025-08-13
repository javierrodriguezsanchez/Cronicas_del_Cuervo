from django.db import models 
from django.contrib.auth.models import User
from main.models import Hilo_models





class Respuesta(models.Model):
    hilo = models.ForeignKey(Hilo_models.Hilo, related_name='respuestas', on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)