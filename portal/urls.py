# -*- coding: utf-8 -*-

'''Reglas para las URIs

'''

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'portada.views.home', name='home'),
                       # Blog
                       url(r'^weblog/', include('zinnia.urls')),
                       url(r'^comments/', include('django.contrib.comments.urls')),
                       # ~~~~
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       (r'^i18n/', include('django.conf.urls.i18n')),
                       )

#from django.conf import settings
#if settings.DEBUG and not settings.PRODUCCION:
#    # FIXME Esto es lo documentado, pero no sirve media
#    #from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#    #urlpatterns += staticfiles_urlpatterns()
#    print "MEDIA %s" % settings.MEDIA_ROOT
#    print "STATIC %s" % settings.STATIC_ROOT
#    urlpatterns += patterns('django.views.static',
#        url(r'^static/(.*)$',  'serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
#        url(r'^media/(.*)$',  'serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
#    )

