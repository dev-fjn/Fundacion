# -*- coding: utf-8 -*-

'''Sistema de menús para django

'''

TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
)


if DEBUG and not PRODUCCION:
    # Desarrollo
    MENU_CACHE_TIME = -1
elif DEBUG and PRODUCCION:
    # Beta
    MENU_CACHE_TIME = -1
else:
    # Producción
    MENU_CACHE_TIME = 1800
