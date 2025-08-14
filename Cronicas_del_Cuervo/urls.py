from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 1) Your app’s URLs go first—no conflicting `admin/` path here:
    path('', include('main.urls')),
]
