from django.db import models 
from django.contrib.auth.models import User
from django import forms
from main.models import Hilo_models, Tags_models
import re


# formulario 
class HiloForm(forms.ModelForm):
    tags_input = forms.CharField(
        label='Etiquetas',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Separadas por comas (ej: programación, django, web)'
        }),
        help_text='Escribe las etiquetas separadas por comas'
    )
    class Meta:
        model = Hilo_models.Hilo
        fields = ['titulo', 'contenido']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['tags_input'].initial = ', '.join(tag.nombre for tag in self.instance.tags.all())
    
    def clean_tags_input(self):
        data = self.cleaned_data['tags_input']
        tag_names = [tag.strip() for tag in re.split(r'[,;]+', data) if tag.strip()]
        return tag_names
    
    def save(self, commit=True):
        # Guardar primero el hilo sin los tags
        hilo = super().save(commit=False)
        
        # Si commit es True, guardar el hilo para obtener ID
        if commit:
            hilo.save()
        
        # Procesar tags solo si el hilo tiene ID
        if hilo.pk:
            tag_names = self.cleaned_data['tags_input']
            tags = []
            for name in tag_names:
                tag, created = Tags_models.Tag.objects.get_or_create(nombre=name)
                tags.append(tag)
            
            # Usar set() para asignar los tags
            hilo.tags.set(tags)
        
        # Si commit es False, necesitamos guardar las relaciones m2m después
        if commit and hasattr(self, 'save_m2m'):
            self.save_m2m()
        
        return hilo
