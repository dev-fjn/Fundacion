# -*- coding: utf-8 -*-

'''Absolute path to the directory static files should be collected to.

Don't put anything  in this directory yourself; store  your static files
in apps' "static/" subdirectories and in STATICFILES_DIRS.

Example: "/home/media/media.lawrence.com/static/"

'''
if DEBUG and not PRODUCCION:
    # Desarrollo
    STATIC_ROOT = PROJECT_ROOT + '/static/'
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
        #os.path.join(PROJECT_ROOT, 'blog/static'),
    )
elif DEBUG and PRODUCCION:
    # Beta
    #STATIC_ROOT = '/var/www/produccion/static'
    #STATIC_URL = '/static/'
    #STATICFILES_DIRS = ()
    pass
else:
    # Producción
    #STATIC_ROOT = '/var/www/pruebas/static'
    #STATIC_URL = '/static/'
    #STATICFILES_DIRS = ()
    pass

