import os
import importlib
from django.db import models as django_models


# Ruta absoluta al directorio actual (models/)
directorio = os.path.dirname(__file__)

for archivo in os.listdir(directorio):
    if archivo.endswith('.py') and archivo != '__init__.py':
        modulo_nombre = f".{archivo[:-3]}"
        modulo = importlib.import_module(modulo_nombre, package=__name__)
        
        # Importar todas las clases que heredan de django.db.models.Model
        for atributo_nombre in dir(modulo):
            atributo = getattr(modulo, atributo_nombre)
            if isinstance(atributo, type) and issubclass(atributo, django_models.Model):
                globals()[atributo_nombre] = atributo