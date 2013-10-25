from django import template
register = template.Library()

from django.conf import settings
from contenidos.models import Imagen, Video

@register.inclusion_tag('contenidos/-imagenes.html')
def imagenes():
    imagenes = Imagen.objects.all()
    return {'MEDIA_URL': settings.MEDIA_URL, 'imagenes': imagenes}

@register.inclusion_tag('contenidos/-videos.html')
def videos():
    return {'MEDIA_URL': settings.MEDIA_URL, "videos": Video.objects.all() }

