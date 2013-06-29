# -*- coding: utf-8 -*-

'''Extensiones para Django.

https://github.com/django-extensions/django-extensions
'''

INSTALLED_APPS += (
    'django_extensions',
)

#MIDDLEWARE_CLASSES += (
#    'flatpages_i18n.middleware.FlatpageFallbackMiddleware',
#)

if DEBUG and not PRODUCCION:
    # Desarrollo
    pass
elif DEBUG and PRODUCCION:
    # Beta
    pass
else:
    # Producción
    pass
