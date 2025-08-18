from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

class Category(models.Model):
    """Categorías para artículos (Economía, Cultura, Ciencias, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        ordering = ("name",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:120]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PublisherProfile(models.Model):
    """
    Perfil adicional para los publicadores. 
    Usa la tabla de User (settings.AUTH_USER_MODEL) para las credenciales.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="publisher_profile")
    nick = models.CharField("nick", max_length=50, unique=True)
    bio = models.TextField("biografía", blank=True)
    phone = models.CharField(max_length=30, blank=True)
    is_approved = models.BooleanField(default=True)  # si el admin aprobó al publicador
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.nick} ({self.user.email})"


class Article(models.Model):
    """Artículo / noticia"""
    STATUS_DRAFT = "draft"
    STATUS_PUBLISHED = "published"
    STATUS_CHOICES = (
        (STATUS_DRAFT, "Borrador"),
        (STATUS_PUBLISHED, "Publicado"),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=260, unique=True, blank=True)
    excerpt = models.CharField(max_length=500, blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="articles")
    categories = models.ManyToManyField(Category, blank=True, related_name="articles")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured_image = models.ImageField(upload_to="articles/images/", blank=True, null=True)

    class Meta:
        ordering = ("-published_at", "-created_at")

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:250]
            slug = base
            counter = 1
            # asegurar unicidad
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        # asignar fecha de publicación si pasa a published y no tiene fecha
        if self.status == self.STATUS_PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Forum(models.Model):
    """Foro general o tópico"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ForumPost(models.Model):
    """Entrada dentro de un foro"""
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="forum_posts")
    title = models.CharField(max_length=250)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    pinned = models.BooleanField(default=False)

    class Meta:
        ordering = ("-pinned", "-created_at")

    def __str__(self):
        return self.title


class WeeklyIssue(models.Model):
    """
    Representa un 'Diario Semanal' que compila varios artículos.
    Por ejemplo: número de la semana o fecha, título principal y lista de artículos.
    """
    title = models.CharField(max_length=250)
    week_start = models.DateField(help_text="Fecha de inicio de la semana/edición")
    articles = models.ManyToManyField(Article, blank=True, related_name="issues")
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to="issues/pdf/", null=True, blank=True)

    class Meta:
        ordering = ("-week_start",)

    def __str__(self):
        return f"Issue {self.week_start} - {self.title}"
    
class Admin(models.Model):
    elemento = models.CharField(max_length=100)

