from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from main.models import Admin

class FormularioEjemplo(forms.Form):
    elemento = forms.CharField(label='Introduce algo')

# Create your views here.
def VistaAdmin(request):
    Lista = [x.elemento for x in Admin.objects.all()]  # Esto obtiene todos los registros
    Lista.reverse()
    if request.method=='POST':
        dato = FormularioEjemplo(request.POST)
        if(dato.is_valid()):
            elemento = dato.cleaned_data['elemento']
            ejemplo = Ejemplo(elemento=elemento)
            ejemplo.save()
            Lista= [elemento]+Lista
    return render(request,'Admin/Admin.html',{
        'form':FormularioEjemplo(),
        'lista':Lista
    })