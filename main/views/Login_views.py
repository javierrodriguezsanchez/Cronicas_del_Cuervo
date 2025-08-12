from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # Redirige a una vista principal
        else:
            return render(request, "Auths/Login_temp.html", {"error": "Credenciales inválidas."})
    return render(request, "Auths/Login_temp.html")
