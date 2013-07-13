# -*- coding: utf-8 -*-

'''Sistema de menús para django

'''
#
#TEMPLATE_CONTEXT_PROCESSORS += (
#        'django.core.context_processors.request',
#)

INSTALLED_APPS += (
    'menus',
)

if DEBUG and not PRODUCCION:
    # Desarrollo
    pass
elif DEBUG and PRODUCCION:
    # Beta
    pass
else:
    # Producción
    pass

