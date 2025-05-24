from django.db import models

class Ejemplo(models.Model):
    elemento = models.CharField(max_length=100)
