import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cronicas_del_cuervo.settings')
django.setup()

from django.contrib.auth.models import User
from main.models import Noticia, Comentario
from django.utils import timezone

def create_sample_data():
    # Create test users
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com', 'password': 'testpass123'}
    )
    
    if created:
        user.set_password('testpass123')
        user.save()

    # Create demo user
    demo_user, created = User.objects.get_or_create(
        username='usuario_demo',
        defaults={
            'email': 'demo@example.com', 
            'password': 'demopass123', 
            'first_name': 'Usuario', 
            'last_name': 'Demo'
        }
    )
    
    if created:
        demo_user.set_password('demopass123')
        demo_user.save()

    # Create sample news
    noticias_data = [
        {
            'titulo': 'Descubrimiento científico revoluciona la medicina',
            'contenido': 'Un equipo de investigadores ha desarrollado una nueva técnica que podría curar enfermedades hasta ahora incurables...',
            'categoria': 'Ciencia'
        },
        {
            'titulo': 'Nuevo récord en el mercado de valores',
            'contenido': 'El índice principal de la bolsa alcanzó su máximo histórico tras los últimos anuncios económicos...',
            'categoria': 'Economía'
        },
        {
            'titulo': 'El equipo local gana el campeonato nacional',
            'contenido': 'En un emocionante partido final, el equipo local se coronó campeón después de 20 años de sequía...',
            'categoria': 'Deportes'
        }
    ]

    for data in noticias_data:
        noticia, created = Noticia.objects.get_or_create(
            titulo=data['titulo'],
            defaults={
                'contenido': data['contenido'],
                'autor': user,
                'categoria': data['categoria'],
                'fecha_publicacion': timezone.now()
            }
        )
        
        # Add some sample comments
        if created:
            comentarios = [
                '¡Increible noticia! Estoy muy emocionado con este avance.',
                '¿Cuándo estará disponible esta tecnología para el público?',
                'Como paciente, esto me da mucha esperanza. Gracias por compartir.'
            ]
            
            for comentario_text in comentarios:
                Comentario.objects.create(
                    noticia=noticia,
                    usuario=user,
                    contenido=comentario_text,
                    fecha=timezone.now()
                )

    print("Datos de muestra creados exitosamente!")

if __name__ == '__main__':
    create_sample_data()