from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Categoria(models.Model):
    """
    Modelo para categorizar os artigos
    Exemplo: Python, Django, React, Carreira
    """
    nome = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nome da categoria (ex: Python, Django)"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="Identificador único para URLs"
    )
    descricao = models.TextField(
        max_length=500,
        blank=True,
        help_text="Descrição opcional da categoria"
    )
    cor = models.CharField(
        max_length=7,
        default="#3498db",
        help_text="Cor em HEX para identidade visual"
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('blog:artigos_por_categoria', args=[self.slug])

    @property
    def total_artigos(self):
        """Retorna o total de artigos publicados na categoria"""
        return self.artigos.filter(publicado=True).count()


class Artigo(models.Model):
    """
    Modelo principal para os artigos do blog
    """
    # Status choices - Boa prática para campos fixos
    STATUS_RASCUNHO = 'rascunho'
    STATUS_REVISAO = 'revisao'
    STATUS_PUBLICADO = 'publicado'

    STATUS_CHOICES = [
        (STATUS_RASCUNHO, 'Rascunho'),
        (STATUS_REVISAO, 'Em Revisão'),
        (STATUS_PUBLICADO, 'Publicado'),
    ]

    # Campos básicos
    titulo = models.CharField(
        max_length=200,
        help_text="Título chamativo para o artigo"
    )
    slug = models.SlugField(
        max_length=200,
        unique_for_date='data_publicacao',
        help_text="URL amigável (gerado automaticamente)"
    )

    # Conteúdo
    resumo = models.TextField(
        max_length=500,
        help_text="Breve resumo para previews e SEO"
    )
    conteudo = models.TextField(
        help_text="Conteúdo principal do artigo (suporta Markdown)"
    )

    # Metadados
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='artigos',
        help_text="Autor do artigo"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        related_name='artigos',
        help_text="Categoria principal do artigo"
    )

    # Status e datas
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_RASCUNHO,
        help_text="Status de publicação"
    )
    destaque = models.BooleanField(
        default=False,
        help_text="Artigo em destaque na homepage"
    )

    data_criacao = models.DateTimeField(auto_now_add=True)
    data_publicacao = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Data de publicação (preenchido automaticamente)"
    )
    data_atualizacao = models.DateTimeField(auto_now=True)

    # SEO e visual
    meta_descricao = models.CharField(
        max_length=300,
        blank=True,
        help_text="Descrição para SEO (até 300 caracteres)"
    )
    imagem_destaque = models.ImageField(
        upload_to='artigos/%Y/%m/',
        blank=True,
        null=True,
        help_text="Imagem de destaque do artigo"
    )
    tempo_leitura = models.PositiveIntegerField(
        default=5,
        help_text="Tempo estimado de leitura em minutos"
    )

    class Meta:
        verbose_name = "Artigo"
        verbose_name_plural = "Artigos"
        ordering = ['-data_publicacao']
        indexes = [
            models.Index(fields=['status', 'data_publicacao']),
            models.Index(fields=['slug', 'data_publicacao']),
        ]

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        if self.data_publicacao:
            return reverse('blog:detalhe_artigo', kwargs={
                'year': self.data_publicacao.year,
                'month': self.data_publicacao.month,
                'day': self.data_publicacao.day,
                'slug': self.slug
            })
        return reverse('blog:detalhe_artigo_rascunho', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        """Auto-preenche data_publicacao quando status muda para publicado"""
        if self.status == self.STATUS_PUBLICADO and not self.data_publicacao:
            self.data_publicacao = timezone.now()
        super().save(*args, **kwargs)

    @property
    def publicado(self):
        return self.status == self.STATUS_PUBLICADO

    @property
    def total_comentarios(self):
        return self.comentarios.filter(aprovado=True).count()