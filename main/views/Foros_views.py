from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404  
from django.http import HttpResponse
from django import forms
from main.models import Hilo_models,Tags_models, Respuesta_models,Foros_models
from django.contrib.auth.decorators import login_required  



# modelos
Hilo = Hilo_models.Hilo
Tag = Tags_models.Tag  
Respuesta = Respuesta_models.Respuesta

def listado_hilos(request,tag_slug=None):
    query = request.GET.get('q', '')
    tag_slug = tag_slug or request.GET.get('tag', '')
    # Base queryset
    hilos = Hilo.objects.all().order_by('-fecha_creacion')
    
    # Aplicar filtros
    if query:
        hilos = hilos.filter(titulo__icontains=query)
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        hilos = hilos.filter(tags=tag)
    
    # Paginación
    paginator = Paginator(hilos, 10)
    page_number = request.GET.get('page')
    hilos_paginados = paginator.get_page(page_number)
    
    # Contexto con mensaje personalizado si no hay resultados
    no_results_message = None
    if not hilos_paginados and query:
        no_results_message = f"No se encontraron hilos para: '{query}'"
    elif not hilos_paginados and tag_slug:
        no_results_message = f"No hay hilos con la etiqueta: '{tag.nombre}'"
    
    return render(request, 'Foros/listado_hilos.html', {
        'hilos': hilos_paginados,
        'no_results_message': no_results_message,
        'query': query,
        'tag_slug': tag_slug
    })

@login_required
def crear_hilo(request):  
    if request.method == 'POST':
        form = Foros_models.HiloForm(request.POST)
        if form.is_valid():
            nuevo_hilo = form.save(commit=False)
            nuevo_hilo.autor = request.user
            nuevo_hilo = form.save()
            return redirect('detalle_hilo', pk=nuevo_hilo.pk)
    else:
        form = Foros_models.HiloForm()
    
    return render(request, 'Foros/crear_hilo.html', {'form': form})


@login_required
def responder_hilo(request, pk):
    hilo = get_object_or_404(Hilo, pk=pk)
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        if contenido:
            Respuesta.objects.create(
                hilo=hilo,
                autor=request.user,
                contenido=contenido
            )
    
    return redirect('detalle_hilo', pk=pk)

def detalle_hilo(request, pk):
    hilo = get_object_or_404(Hilo, pk=pk)
    return render(request, 'Foros/detalle_hilo.html', {'hilo': hilo})
