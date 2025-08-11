from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from main.models import Admin

# Create your views here.
def VistaAdmin(request):
    return render(request,'Admin/Admin.html',{
    })