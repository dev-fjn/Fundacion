# -*- coding: utf-8 -*-

'''Formulario de contacto para django

'''
#
#TEMPLATE_CONTEXT_PROCESSORS += (
#        'django.core.context_processors.request',
#)

INSTALLED_APPS += (
    'django_contactme',
)

# Las url's se añadieron al fichero portal/urls.py

if DEBUG and not PRODUCCION:
    # Desarrollo
    pass
elif DEBUG and PRODUCCION:
    # Beta
    pass
else:
    # Producción
    pass

