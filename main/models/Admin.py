from django.db import models

class Admin(models.Model):
    elemento = models.CharField(max_length=100)
