from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Artigo, Categoria


def lista_artigos(request):
    """Página inicial - lista todos os artigos publicados"""
    artigos = Artigo.objects.filter(status=Artigo.STATUS_PUBLICADO)

    return render(request, 'blog/lista_artigos.html', {
        'artigos': artigos,
        'titulo': 'Artigos Recentes'
    })


def artigos_por_categoria(request, slug):
    """Lista artigos de uma categoria específica"""
    categoria = get_object_or_404(Categoria, slug=slug)
    artigos = Artigo.objects.filter(
        categoria=categoria,
        status=Artigo.STATUS_PUBLICADO
    )

    return render(request, 'blog/lista_artigos.html', {
        'artigos': artigos,
        'titulo': f'Artigos em {categoria.nome}',
        'categoria': categoria
    })


def detalhe_artigo(request, year, month, day, slug):
    """Página de detalhe de um artigo publicado"""
    artigo = get_object_or_404(
        Artigo,
        slug=slug,
        data_publicacao__year=year,
        data_publicacao__month=month,
        data_publicacao__day=day,
        status=Artigo.STATUS_PUBLICADO
    )

    return render(request, 'blog/detalhe_artigo.html', {
        'artigo': artigo
    })


def detalhe_artigo_rascunho(request, pk):
    """Página para visualizar rascunhos (acesso restrito)"""
    artigo = get_object_or_404(Artigo, pk=pk)

    # Verificar se usuário tem permissão (autor ou staff)
    if not request.user.is_authenticated or (request.user != artigo.autor and not request.user.is_staff):
        return HttpResponse('Acesso negado', status=403)

    return render(request, 'blog/detalhe_artigo.html', {
        'artigo': artigo
    })


def sobre(request):
    """Página Sobre"""
    return render(request, 'blog/sobre.html', {
        'titulo': 'Sobre o CMS Moderno'
    })


def contato(request):
    """Página Contato"""
    return render(request, 'blog/contato.html', {
        'titulo': 'Contato'
    })