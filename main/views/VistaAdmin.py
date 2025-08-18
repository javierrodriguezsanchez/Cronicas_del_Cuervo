import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_http_methods

from .models import PublisherProfile, Article, Category, Forum, WeeklyIssue

User = get_user_model()

def staff_required(user):
    return user.is_active and user.is_staff

@user_passes_test(staff_required, login_url="/login/")
@require_http_methods(["GET", "POST"])
def admin_dashboard(request):
    """
    Vista principal del Admin. - GET: devuelve plantilla con TODOS los datos necesarios.
    - POST: soporta acciones simples: crear publicador, reiniciar contraseña, borrar publicador.
      Debes enviar un campo 'action' en el formulario: add_publisher | reset_password | delete_publisher
    """
    # ---------- Manejo de acciones POST ----------
    if request.method == "POST":
        action = request.POST.get("action", "")
        if action == "add_publisher":
            email = request.POST.get("email", "").strip()
            nick = request.POST.get("nick", "").strip()
            if not email or not nick:
                messages.error(request, "Email y Nick son requeridos.")
                return redirect(reverse("admin_dashboard"))

            # generar contraseña segura de forma aleatoria
            pwd = get_random_string(length=12)
            # usar username = email para facilidad (si tu proyecto necesita otra cosa, ajusta)
            user, created = User.objects.get_or_create(email=email, defaults={"username": email})
            if not created:
                messages.error(request, f"Ya existe un usuario con {email}.")
                return redirect(reverse("admin_dashboard"))

            user.set_password(pwd)
            user.is_active = True
            user.save()
            # crear perfil
            PublisherProfile.objects.create(user=user, nick=nick)
            # Guardamos la contraseña temporalmente en sesión para mostrarla una vez en la UI
            request.session["generated_password_for"] = email
            request.session["generated_password_value"] = pwd
            messages.success(request, f"Publicador {nick} creado.")
            return redirect(reverse("admin_dashboard"))

        elif action == "reset_password":
            email = request.POST.get("email", "").strip()
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Usuario no encontrado.")
                return redirect(reverse("admin_dashboard"))
            new_pwd = get_random_string(length=12)
            user.set_password(new_pwd)
            user.save()
            request.session["generated_password_for"] = email
            request.session["generated_password_value"] = new_pwd
            messages.success(request, f"Contraseña reiniciada para {email}.")
            return redirect(reverse("admin_dashboard"))

        elif action == "delete_publisher":
            email = request.POST.get("email", "").strip()
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Usuario no encontrado.")
                return redirect(reverse("admin_dashboard"))
            # borrado definitivo: primero perfil
            PublisherProfile.objects.filter(user=user).delete()
            user.delete()
            messages.success(request, f"Publicador {email} eliminado.")
            return redirect(reverse("admin_dashboard"))

        else:
            messages.warning(request, "Acción no reconocida.")
            return redirect(reverse("admin_dashboard"))

    # ---------- GET: Construir contexto completo ----------
    publishers_qs = PublisherProfile.objects.select_related("user").all()
    publishers = []
    for p in publishers_qs:
        publishers.append({
            "nick": p.nick,
            "email": p.user.email,
            "is_active": p.user.is_active,
            "created_at": p.created_at.isoformat(),
        })

    latest_articles = list(Article.objects.filter(status=Article.STATUS_PUBLISHED)
                           .select_related("author")
                           .order_by("-published_at")[:10]
                           .values("title", "slug", "published_at", "author__email"))

    categories = list(Category.objects.all().values("name", "slug"))
    forums = list(Forum.objects.all().values("title", "slug", "created_at"))
    latest_issue = WeeklyIssue.objects.order_by("-week_start").first()

    context = {
        "publishers_json": json.dumps(publishers),   # para que el front lo consuma
        "publishers_count": len(publishers),
        "latest_articles": latest_articles,
        "latest_articles_count": len(latest_articles),
        "categories": categories,
        "forums": forums,
        "latest_issue": {
            "title": latest_issue.title,
            "week_start": latest_issue.week_start.isoformat(),
            "published": latest_issue.published,
        } if latest_issue else None,
        # Si generamos una contraseña hace poco la mostramos una vez
        "generated_password_for": request.session.pop("generated_password_for", None),
        "generated_password_value": request.session.pop("generated_password_value", None),
    }

    return render(request, "Admin.html", context)