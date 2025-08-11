from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def registro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}! Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
            # En lugar de redirigir, mostramos los errores en el mismo template
            return render(request, 'Autentificar/Registro_temp.html', {'form': form})
    
    # GET request: mostrar formulario vacío
    form = UserCreationForm()
    return render(request, 'Autentificar/Registro_temp.html', {'form': form})


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}! Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
            return redirect('login')

    else:
        messages.warning(request, f'¡Cuenta no creada! Ahora NO puedes iniciar sesión.')
        form = UserCreationForm()
    return render(request, 'Autentificar/Registro_temp.html', {'form': form})