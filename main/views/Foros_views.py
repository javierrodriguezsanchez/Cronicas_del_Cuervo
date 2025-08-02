from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404  
from django.http import HttpResponse
from django import forms
from main.models import Foros_models
from django.contrib.auth.decorators import login_required  
#aqui hay que crear el crearhilo,detalle_hilo,buscar_hilos
"""
Hilo= Foros_models.Hilo 
def listado_hilos(request):
    query = request.GET.get('q', '')
    hilos_list = Hilo.objects.all()
    
    if query:
        hilos_list = hilos_list.filter(titulo__icontains=query)
    
    paginator = Paginator(hilos_list, 10)  # 10 hilos por página
    page_number = request.GET.get('page')
    hilos = paginator.get_page(page_number)
    
    return render(request, 'Foros/listado.html', {'hilos': hilos})


def crear_hilo(request):  
    if request.method == 'POST':
        form = HiloForm(request.POST)
        if form.is_valid():
            nuevo_hilo = form.save(commit=False)
            nuevo_hilo.autor = request.user
            nuevo_hilo.save()
            form.save_m2m()  # Para guardar ManyToMany (tags)
            return redirect('detalle_hilo', pk=nuevo_hilo.pk)
    else:
        form = HiloForm()
    
    return render(request, 'Foros/crear_hilo.html', {'form': form})

"""



# modelos
Hilo = Foros_models.Hilo
Tag = Foros_models.Tag  

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

# Vista para listar hilos
def listado_hilos(request):
    query = request.GET.get('q', '')
    hilos_list = Hilo.objects.all().order_by('-fecha_creacion')
    
    if query:
        hilos_list = hilos_list.filter(titulo__icontains=query)
    
    paginator = Paginator(hilos_list, 10)  
    page_number = request.GET.get('page',1)
    
    try:
        hilos = paginator.page(page_number)
    except PageNotAnInteger:
        hilos = paginator.page(1)
    except EmptyPage:
        hilos = paginator.page(paginator.num_pages)

    try:
        page_number = int(page_number)
    except (TypeError, ValueError):
        page_number = 1
    
    try:
        hilos = paginator.page(page_number)
    except PageNotAnInteger:
        hilos = paginator.page(1)
    except EmptyPage:
        hilos = paginator.page(paginator.num_pages)
    
    return render(request, 'Foros/listado.html', {'hilos': hilos})
    

@login_required
def crear_hilo(request):  
    if request.method == 'POST':
        form = HiloForm(request.POST)
        if form.is_valid():
            nuevo_hilo = form.save(commit=False)
            nuevo_hilo.autor = request.user
            nuevo_hilo.save()
            form.save_m2m()  # Para guardar ManyToMany (tags)
            return redirect('detalle_hilo', pk=nuevo_hilo.pk)
    else:
        form = HiloForm()
    
    return render(request, 'Foros/crear_hilo.html', {'form': form})

# Vista para detalle de hilo
def detalle_hilo(request, pk):
    hilo = get_object_or_404(Hilo, pk=pk)
    return render(request, 'Foros/detalle_hilo.html', {'hilo': hilo})

# Vista para búsqueda (puede usar la misma de listado)
def buscar_hilos(request):
    # Reutilizamos la lógica de listado_hilos
    return listado_hilos(request)