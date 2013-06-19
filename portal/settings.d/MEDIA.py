# -*- coding: utf-8 -*-

'''Absolute filesystem path to the directory that will hold user-uploaded files.

Example: "/home/media/media.lawrence.com/media/"

'''
#MEDIA_ROOT += os.path.normpath(os.path.join(os.path.dirname(__file__),"../media/"))
if DEBUG and not PRODUCCION:
    MEDIA_ROOT = os.path.join(PROJECT_ROOT,'media')
elif DEBUG and PRODUCCION:
    MEDIA_ROOT = '/var/www/produccion/media'
else:
    MEDIA_ROOT = '/var/www/pruebas/media'

'''URL that handles the media served from MEDIA_ROOT. Make sure to use a trailing slash.

Examples: "http://media.lawrence.com/media/", "http://example.com/media/"

'''

#MEDIA_URL += 'http://127.0.0.1/media/'
#MEDIA_URL += '/media/'

