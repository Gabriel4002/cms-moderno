from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Página inicial - lista de artigos
    path('', views.lista_artigos, name='lista_artigos'),

    # Artigo por categoria
    path('categoria/<slug:slug>/', views.artigos_por_categoria, name='artigos_por_categoria'),

    # Detalhe do artigo (com data na URL)
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.detalhe_artigo,
         name='detalhe_artigo'),

    # Detalhe de rascunho (sem data de publicação)
    path('rascunho/<int:pk>/',
         views.detalhe_artigo_rascunho,
         name='detalhe_artigo_rascunho'),

    # Páginas estáticas
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
]