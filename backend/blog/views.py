from django.shortcuts import render
from django.http import HttpResponse

def lista_artigos(request):
    return HttpResponse("""
    <h1>🚀 CMS Moderno 2025</h1>
    <p>Bem-vindo ao nosso CMS com Django 5.2.7 + Python 3.13.5!</p>
    <p><a href='/admin/'>Acessar Admin</a></p>
    """)