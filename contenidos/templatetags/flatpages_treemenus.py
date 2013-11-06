# -*- coding: utf-8 -*-

from django import template
register = template.Library()

from treemenus.models import Menu, MenuItem


@register.simple_tag(takes_context=True)
def enlace_a_pagina_padre_en_menu(context):
    ruta = context['request'].META['PATH_INFO']
    try:
        submenu = Menu.objects.get(name="principal").contained_items.get(url=ruta)
        padre = submenu.parent
        return '<a href="%s">%s</a>' % (padre.url, padre.caption,)
    except MenuItem.DoesNotExist:
        return ''
