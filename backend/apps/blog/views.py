from django.shortcuts import render
from django.http import HttpResponse

def lista_artigos(request):
    return render(request, 'blog/home.html', {
        'titulo': 'CMS Moderno 2025',
        'mensagem': 'Bem-vindo ao nosso blog moderno!'
    })

def sobre(request):
    return HttpResponse("<h1>Sobre Nós</h1><p>CMS com Django 5.2.7</p>")

def contato(request):
    return HttpResponse("<h1>Contato</h1><p>Entre em contato conosco.</p>")