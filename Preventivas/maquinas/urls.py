# IMPORTA PATH DE DJANGO E IMPORTA OS COMPONENTES DE views.py PARA SEREM USADOS AQUI 
from django.urls import path
from . import views


# CRIA UMA LISTA COM AS URLS
urlpatterns = [
    # URL QUE DIRECIONA PARA A PÁGINA INDEX
    path('', views.index, name='index'),

    # URL QUE DIRECIONA PARA A PÁGINA DE ADICIONAR PREVENTIVA
    path('nova_prev', views.nova_prev, name='addPrev'),

    # URL QUE DIRECIONA PARA A PÁGINA DE COMPARAR HORIMETROS
    path('CompPrev', views.CompPrev, name='CompPrev'),

    # URL QUE DIRECIONA PARA A PÁGINA DE PECAS USADAS, USA COMO PARAMETRO O ID QUE SERÁ PASSADO NA URL
    path('pecas/<pecas_id>/', views.pecas, name='pecas'),

    # URL QUE DIRECIONA PARA A PÁGINA DE MÁQUINAS QUE PRECISAM DE PREVENTIVA.
    path('pendentes', views.pendentes, name='pendentes')

]
