# -*- coding: utf-8 -*-

from django import template
register = template.Library()

from contenidos.models import Imagen, Video, Evento, FechaEvento
from contenidos.utiles import inicio_fin_mes, calendario_por_meses
from django.conf import settings
from django.utils import timezone
from zinnia.models import Category
import datetime

@register.inclusion_tag('contenidos/_imagenes.html')
def imagenes():
    imagenes = Imagen.objects.all()
    return {'MEDIA_URL': settings.MEDIA_URL, 'imagenes': imagenes}

@register.inclusion_tag('contenidos/_videos.html')
def videos():
    return {'MEDIA_URL': settings.MEDIA_URL, "videos": Video.objects.all() }

@register.inclusion_tag('contenidos/_proximos_eventos.html', takes_context=True)
def proximos_eventos(context, cuenta):
    cuenta = int(cuenta)
    start = timezone.now()
    #end = start+datetime.timedelta(days=60)
    # buscar eventos en rango
    qs = FechaEvento.objects.filter(fecha__gte=start) #, fecha__lte=end)
    return {
            'user': context.get('user'),
            'object_list': qs[:cuenta], 
        }

@register.inclusion_tag('contenidos/_calendario_eventos.html', takes_context=True)
def calendario_eventos(context, meses_atras):
    start, end = inicio_fin_mes(meses_atras)
    diccionario = Evento.datos_para_calendario(start, end)
    semanas = calendario_por_meses(start, end, diccionario)
    return {
            'user': context.get('user'),
            'only': True,
            'hoy': timezone.now().date(), 
            'start': start, 
            'semanas': semanas, 
            'prev': start-datetime.timedelta(days=1), 
            'next': end+datetime.timedelta(days=1),
        }

@register.inclusion_tag('contenidos/_resumen_de_zinnia.html', takes_context=True)
def resumen_de_zinnia(context, category_slug):
    c = Category.objects.get(slug=category_slug)
    return {
        'user': context.get('user'),
        'category': c,
        'object_list': c.entries_published(),
    }

