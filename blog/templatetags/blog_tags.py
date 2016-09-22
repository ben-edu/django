# -*- coding: utf-8 -*-
# blog/templatetags/blog_tags.py

from django import template

from ..models import Article, Tag

register = template.Library()


@register.inclusion_tag('blog/_menus.html')
def get_menus_blog():
    context = {
        # Obtener lista completa de etiquetas
        'lista_tags': Tag.objects.all(),
        # Obtener las 5 ultimas entradas
        'ultimos_articulos': Article.objects.order_by('-create_at')[:5]
    }
    return context