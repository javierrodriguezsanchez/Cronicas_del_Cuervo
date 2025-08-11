from django.db import models 
from django.contrib.auth.models import User
from django import forms



class Hilo(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    cerrado = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag',blank= True)
    

    @property
    def ultima_respuesta(self):
        if self.respuestas.exists():
            return self.respuestas.latest('fecha_creacion').fecha_creacion
        return self.fecha_creacion


class Respuesta(models.Model):
    hilo = models.ForeignKey(Hilo, related_name='respuestas', on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    nombre = models.CharField(max_length=50, unique=True)


# formulario 
class HiloForm(forms.ModelForm):
    class Meta:
        model = Hilo
        fields = ['titulo', 'contenido', 'tags']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Escribe el contenido de tu hilo aquí...',
                'class': 'form-control'
            }),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.all()
        self.fields['tags'].required = False
