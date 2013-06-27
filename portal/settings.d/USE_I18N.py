# -*- coding: utf-8 -*-

'''If you set  this to False, Django will make  some optimizations so as
not to load the internationalization machinery.

'''

USE_I18N = True

# A string representing the language code for this installation.
LANGUAGE_CODE = 'en'

LANGUAGE_COOKIE_NAME = 'Lang site: '

LANGUAGE_BIDI = False

# ESTO PUEDE DAR LA LATA La documentacion
# https://docs.djangoproject.com/en/1.0/topics/i18n/ dice que te
# asegures de que es uno de los primeros middlewares, pero que debe ir
# despues de sessionmiddleware y de cachemiddleware.

MIDDLEWARE_CLASSES += ( 'django.middleware.locale.LocaleMiddleware',)

LOCALE_PATHS = (os.path.join(os.path.dirname(os.path.dirname(__file__)), 'conf/locale'), )

ugettext = lambda s: s
LANGUAGES = (
    ('es', ugettext(u'Spanish')),
    ('en', ugettext(u'English')),
)

#
# chuleta
# 
# ./python.sh manage.py  makemessages -l en -e "html,js,txt" --ignore='virtualenv/*' 
# ./python.sh manage.py  makemessages -l es -e "html,js,txt" --ignore='virtualenv/*' 
# vimdiff conf/locale/e?/LC_MESSAGES/django.po 
# ./python.sh manage.py compilemessages 
# 
