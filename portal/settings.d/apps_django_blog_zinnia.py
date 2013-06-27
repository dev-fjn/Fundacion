# -*- coding: utf-8 -*-

'''Sistema de blog empotrable.

'''

INSTALLED_APPS += (
    'django.contrib.comments',
    'django.contrib.sitemaps',
    'mptt',
    'tagging',
    'zinnia',
)

TEMPLATE_CONTEXT_PROCESSORS += (
      'zinnia.context_processors.version',
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
