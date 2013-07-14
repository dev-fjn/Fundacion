# -*- coding: utf-8 -*-

'''Modified Preorder Tree Traversal ( mptt )

Sistema para  almacenar datos jerarquicos en una BBDD.
'''
#
#TEMPLATE_CONTEXT_PROCESSORS += (
#        'django.core.context_processors.request',
#)

INSTALLED_APPS += (
    'mptt',
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

