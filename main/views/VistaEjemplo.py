from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from main.models import Ejemplo

class FormularioEjemplo(forms.Form):
    elemento = forms.CharField(label='Introduce algo')

# Create your views here.
def VistaEjemplo(request):
    Lista = [x.elemento for x in Ejemplo.objects.all()]  # Esto obtiene todos los registros
    Lista.reverse()
    if request.method=='POST':
        dato = FormularioEjemplo(request.POST)
        if(dato.is_valid()):
            elemento = dato.cleaned_data['elemento']
            ejemplo = Ejemplo(elemento=elemento)
            ejemplo.save()
            Lista= [elemento]+Lista
    return render(request,'Ejemplo/ejemplo.html',{
        'form':FormularioEjemplo(),
        'lista':Lista
    })