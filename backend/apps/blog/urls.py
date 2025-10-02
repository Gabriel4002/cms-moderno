from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.lista_artigos, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
]