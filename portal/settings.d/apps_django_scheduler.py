# -*- coding: utf-8 -*-

'''Eventos + Calendario.

'''

INSTALLED_APPS += (
    'django_nose',
    'schedule',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

FIRST_DAY_OF_WEEK = 1

# OCCURRENCE_CANCEL_REDIRECT

# SHOW_CANCELLED_OCCURRENCES = False

# CHECK_PERMISSION_FUNC

# GET_EVENTS_FUNC

if DEBUG and not PRODUCCION:
    # Desarrollo
    pass
elif DEBUG and PRODUCCION:
    # Beta
    pass
else:
    # Producción
    pass
