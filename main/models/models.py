from django.db import models
from django.contrib.auth import get_user_model
from django import forms





User = get_user_model()

class Categoría(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Etiquetas(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Autor(models.Model):
    full_name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.full_name

class Noticia(models.Model):
    título          = models.CharField(max_length=255)
    contenido       = models.TextField()
    autores        = models.ManyToManyField(Autor, related_name='articles')
    etiquetas      = models.ManyToManyField(Etiquetas, related_name='all_news')
    categoría      = models.ForeignKey(Categoría, on_delete=models.PROTECT, related_name='articles')
    fecha_de_publicación = models.DateField()

    def __str__(self):
        return self.title

class WeeklyJournal(models.Model):
    file = models.FileField(upload_to='journals/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Journal uploaded on {self.uploaded_at.date()}"
    
class WeeklyJournalForm(forms.ModelForm):
    class Meta:
        model = WeeklyJournal
        fields = ['file']
