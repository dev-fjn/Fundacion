# -*- coding: utf-8 -*-

'''Sistema de logueo personalizado.

Más detallado que el sistema que viene a modo de ejemplo.'''

if DEBUG and PRODUCCION:

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'django.utils.log.NullHandler',
            },
            'console':{
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
            'django.db': {
                'handlers': ['null'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'gunicorn.error': {
                'handlers': ['null'],
                'propagate': False,
            },
            '': {
                'handlers': ['console'],
                'level': 'INFO',
            }
        }
    }

# Configuracion para los petes por correo
    import socket
    EMAIL_SUBJECT_PREFIX = "cafeteria@" + socket.gethostname() + ": "
    SERVER_EMAIL = "cafeteria@" + socket.getfqdn(socket.gethostname())


