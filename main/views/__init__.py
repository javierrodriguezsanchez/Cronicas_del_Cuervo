import os
import importlib

directorio = os.path.dirname(__file__)

for archivo in os.listdir(directorio):
    if archivo.endswith('.py') and archivo != '__init__.py':
        modulo_nombre = f".{archivo[:-3]}"
        modulo = importlib.import_module(modulo_nombre, package=__name__)
        for nombre in dir(modulo):
            if not nombre.startswith('_'):
                globals()[nombre] = getattr(modulo, nombre)
