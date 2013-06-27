# -*- coding: utf-8 -*-

'''Páginas estáticas, con soporte para i18n.

Configurado según:
https://pypi.python.org/pypi/django-flatpages-i18n
'''

INSTALLED_APPS += (
    'modeltranslation',
    'flatpages_i18n',
)

MIDDLEWARE_CLASSES += (
    'flatpages_i18n.middleware.FlatpageFallbackMiddleware',
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
