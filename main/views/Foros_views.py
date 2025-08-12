from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404  
from django.http import HttpResponse
from django import forms
from main.models import Foros_models
from django.contrib.auth.decorators import login_required  

# modelos
Hilo = Foros_models.Hilo
Tag = Foros_models.Tag  



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
        form = Foros_models.HiloForm(request.POST)
        if form.is_valid():
            nuevo_hilo = form.save(commit=False)
            nuevo_hilo.autor = request.user
            nuevo_hilo.save()
            form.save_m2m()  # Para guardar ManyToMany (tags)
            return redirect('detalle_hilo', pk=nuevo_hilo.pk)
    else:
        form = Foros_models.HiloForm()
    
    return render(request, 'Foros/crear_hilo.html', {'form': form})


# main/views/Foros_views.py
from django.shortcuts import redirect, get_object_or_404
from main.models import Foros_models
from django.contrib.auth.decorators import login_required

Respuesta = Foros_models.Respuesta

@login_required  # Comenta esto temporalmente si quieres probar sin login
def responder_hilo(request, pk):
    """Vista temporal para respuestas sin autenticación"""
    # Obtener el hilo
    hilo = get_object_or_404(Hilo, pk=pk)
    
    # Asignar usuario temporal si no hay autenticación
    if not request.user.is_authenticated:
        from django.contrib.auth.models import User
        default_user = User.objects.first() or User.objects.create_user(
            'temp_user', 'temp@example.com', 'temp_pass'
        )
    else:
        default_user = request.user
    
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        if contenido:
            # Crear la respuesta
            Respuesta.objects.create(
                hilo=hilo,
                autor=default_user,
                contenido=contenido
            )
    
    return redirect('detalle_hilo', pk=pk)

# Vista para detalle de hilo
def detalle_hilo(request, pk):
    hilo = get_object_or_404(Hilo, pk=pk)
    return render(request, 'Foros/detalle_hilo.html', {'hilo': hilo})

# Vista para búsqueda (puede usar la misma de listado)
def buscar_hilos(request):
    return listado_hilos(request)