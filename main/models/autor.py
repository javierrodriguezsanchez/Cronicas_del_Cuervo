from django.db import models

class Autor(models.Model):
    full_name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.full_name