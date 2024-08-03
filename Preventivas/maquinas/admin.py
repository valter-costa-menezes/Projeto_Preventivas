from django.contrib import admin
from maquinas.models import Patrimonio
from maquinas.models import UltimaPreventiva

# DEFINE OS MODELS PRESENTES NA PAGINA ADMINISTRATIVA
admin.site.register(Patrimonio)
admin.site.register(UltimaPreventiva)
