# -*- coding: utf-8 -*-

'''Absolute path to the directory static files should be collected to.

Don't put anything  in this directory yourself; store  your static files
in apps' "static/" subdirectories and in STATICFILES_DIRS.

Example: "/home/media/media.lawrence.com/static/"

'''
if DEBUG and not PRODUCCION:
    STATIC_ROOT = PROJECT_ROOT + '/static/'
elif DEBUG and PRODUCCION:
    STATIC_ROOT = '/var/www/fjn_beta/static'
else:
    STATIC_ROOT = '/var/www/fjn_www/static'

STATIC_URL = '/static/'
STATICFILES_DIRS = ()

