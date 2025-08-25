import json
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from main.models import Noticia, Comentario
from django.middleware.csrf import get_token
from django.contrib.auth.models import User  # Añade esta importación

# Modo demo - permite probar sin autenticación completa
MODO_DEMO = True  # Cambiar a False en producción

def comentarios_noticias(request):
    # Obtener todas las noticias
    noticias = Noticia.objects.all().order_by('-fecha_publicacion')

    noticias_json = [
        {
            'id': noticia.id,
            'titulo': noticia.titulo,
            'categoria': noticia.categoria,
            'fecha_publicacion': timezone.localtime(noticia.fecha_publicacion).strftime("%d/%m/%Y"),
            'autor': noticia.autor.username,
            'contenido': noticia.contenido,
            'likes': noticia.likes,
            'dislikes': noticia.dislikes
        }
        for noticia in noticias
    ]

    # Obtener noticia seleccionada
    noticia_id = request.GET.get('noticia_id')
    noticia_seleccionada = None
    comentarios = []
    
    # Manejar noticia seleccionada 
    if noticia_id:
        try:
            noticia_seleccionada = Noticia.objects.get(id=noticia_id)
        except Noticia.DoesNotExist:
            return JsonResponse({'error': 'Noticia no encontrada'}, status=404)
        
        # Obtener comentarios
        comentarios = Comentario.objects.filter(
            noticia=noticia_seleccionada, 
            comentario_padre__isnull=True
        ).order_by('-fecha')
    
    # Manejar reacciones
    usuario_ha_dado_like = False
    usuario_ha_dado_dislike = False
    
    if noticia_seleccionada and request.user.is_authenticated:
        usuario_ha_dado_like = request.user in noticia_seleccionada.usuarios_like.all()
        usuario_ha_dado_dislike = request.user in noticia_seleccionada.usuarios_dislike.all()
    elif MODO_DEMO and noticia_seleccionada:
        # En modo demo, simular estado de reacciones
        usuario_ha_dado_like = request.session.get(f'news_{noticia_id}_like', False)
        usuario_ha_dado_dislike = request.session.get(f'news_{noticia_id}_dislike', False)
    
    # Convertir comentarios a JSON para el frontend
    comentarios_json = []
    for comentario in comentarios:
        user_like = False
        if request.user.is_authenticated:
            user_like = request.user in comentario.usuarios_like.all()
        elif MODO_DEMO:
            user_like = request.session.get(f'comment_{comentario.id}_like', False)
            
        comentarios_json.append({
            'id': comentario.id,
            'usuario': comentario.usuario.username,
            'contenido': comentario.contenido,
            'fecha': comentario.fecha.strftime("%d/%m/%Y %H:%M"),
            'likes': comentario.likes,
            'user_like': user_like
        })
    
    # Obtener token CSRF
    csrf_token = get_token(request)
    
    # Convertir a JSON para el frontend
    noticias_json_str = json.dumps(noticias_json)
    comentarios_json_str = json.dumps(comentarios_json)
    
    # Usuario demo para pruebas
    usuario_demo = None
    if MODO_DEMO and not request.user.is_authenticated:
        # Crear o obtener usuario demo para pruebas
        usuario_demo, created = User.objects.get_or_create(
            username='usuario_demo',
            defaults={'first_name': 'Usuario', 'last_name': 'Demo'}
        )
    
    return render(request, 'comentarios/comment_section_2.html', {
        'noticias': noticias,
        'noticias_json_str': noticias_json_str,
        'comentarios_json_str': comentarios_json_str,
        'noticia_seleccionada': noticia_seleccionada,
        'comentarios': comentarios,
        'usuario_autenticado': request.user.is_authenticated,
        'usuario_ha_dado_like': usuario_ha_dado_like,
        'usuario_ha_dado_dislike': usuario_ha_dado_dislike,
        'csrf_token': csrf_token,
        'modo_demo': MODO_DEMO,
        'usuario_demo': usuario_demo
    })

@require_POST
def agregar_comentario(request):
    # En modo demo, permitir comentarios sin autenticación
    if MODO_DEMO and not request.user.is_authenticated:
        # Usar usuario demo para comentarios en modo prueba
        from django.contrib.auth.models import User
        usuario_demo, created = User.objects.get_or_create(
            username='usuario_demo',
            defaults={'first_name': 'Usuario', 'last_name': 'Demo'}
        )
        request.user = usuario_demo
    
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Usuario no autenticado'}, status=403)
    
    # Obtener datos directamente del POST
    contenido = request.POST.get('contenido')
    noticia_id = request.POST.get('noticia')
    comentario_padre_id = request.POST.get('comentario_padre')
    
    # Validar contenido
    if not contenido:
        return JsonResponse({'success': False, 'error': 'El contenido no puede estar vacío'}, status=400)
    
    # Validar que exista la noticia
    try:
        noticia = Noticia.objects.get(id=noticia_id)
    except Noticia.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Noticia no encontrada'}, status=404)
    
    # Manejar comentario padre correctamente
    comentario_padre = None
    if comentario_padre_id and comentario_padre_id != '':
        try:
            comentario_padre = Comentario.objects.get(id=comentario_padre_id)
        except Comentario.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Comentario padre no encontrado'}, status=404)
    
    # Crear el comentario
    comentario = Comentario(
        noticia=noticia,
        usuario=request.user,
        contenido=contenido,
        comentario_padre=comentario_padre
    )
    comentario.save()
    
    return JsonResponse({
        'success': True,
        'comentario_id': comentario.id,
        'usuario': request.user.username,
        'contenido': contenido,
        'fecha': comentario.fecha.strftime("%d/%m/%Y %H:%M"),
        'es_respuesta': bool(comentario_padre)
    })

@require_POST
def manejar_reaccion(request):
    # En modo demo, permitir reacciones sin autenticación
    if MODO_DEMO and not request.user.is_authenticated:
        # Usar usuario demo para reacciones en modo prueba
        from django.contrib.auth.models import User
        usuario_demo, created = User.objects.get_or_create(
            username='usuario_demo',
            defaults={'first_name': 'Usuario', 'last_name': 'Demo'}
        )
        request.user = usuario_demo
    
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Usuario no autenticado'}, status=403)
    
    tipo = request.POST.get('tipo')
    objeto_id = request.POST.get('id')
    accion = request.POST.get('accion')
    usuario = request.user
    
    if tipo == 'noticia':
        noticia = get_object_or_404(Noticia, id=objeto_id)

        if accion == 'like':
            if usuario in noticia.usuarios_like.all():
                noticia.usuarios_like.remove(usuario)
                # Guardar estado en sesión para modo demo
                if MODO_DEMO:
                    request.session[f'news_{objeto_id}_like'] = False
            else:
                noticia.usuarios_like.add(usuario)
                noticia.usuarios_dislike.remove(usuario)
                # Guardar estado en sesión para modo demo
                if MODO_DEMO:
                    request.session[f'news_{objeto_id}_like'] = True
                    request.session[f'news_{objeto_id}_dislike'] = False

        elif accion == 'dislike':
            if usuario in noticia.usuarios_dislike.all():
                noticia.usuarios_dislike.remove(usuario)
                # Guardar estado en sesión para modo demo
                if MODO_DEMO:
                    request.session[f'news_{objeto_id}_dislike'] = False
            else:
                noticia.usuarios_dislike.add(usuario)
                noticia.usuarios_like.remove(usuario)
                # Guardar estado en sesión para modo demo
                if MODO_DEMO:
                    request.session[f'news_{objeto_id}_dislike'] = True
                    request.session[f'news_{objeto_id}_like'] = False

        return JsonResponse({
            'likes': noticia.usuarios_like.count(),
            'dislikes': noticia.usuarios_dislike.count(),
            'user_like': usuario in noticia.usuarios_like.all(),
            'user_dislike': usuario in noticia.usuarios_dislike.all()
        })

    elif tipo == 'comentario':
        comentario = get_object_or_404(Comentario, id=objeto_id)
        if usuario in comentario.usuarios_like.all():
            comentario.usuarios_like.remove(usuario)
            # Guardar estado en sesión para modo demo
            if MODO_DEMO:
                request.session[f'comment_{objeto_id}_like'] = False
        else:
            comentario.usuarios_like.add(usuario)
            # Guardar estado en sesión para modo demo
            if MODO_DEMO:
                request.session[f'comment_{objeto_id}_like'] = True

        return JsonResponse({
            'likes': comentario.usuarios_like.count(),
            'user_like': usuario in comentario.usuarios_like.all()
        })
    
    return JsonResponse({'error': 'Tipo no válido'}, status=400)