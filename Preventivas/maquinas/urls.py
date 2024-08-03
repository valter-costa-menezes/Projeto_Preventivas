from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nova_prev', views.nova_prev, name='addPrev'),
    path('CompPrev', views.CompPrev, name='CompPrev'),
    path('pecas/<pecas_id>/', views.pecas, name='pecas'),
    path('pendentes', views.pendentes, name='pendentes')

]
