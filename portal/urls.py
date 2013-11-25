# -*- coding: utf-8 -*-

'''Reglas para las URIs

'''

from django.conf import settings
from django.contrib import admin
from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.views.generic.base import TemplateView

# Soporte para robots.txt && favicon.ico
#from django.views.generic.simple import direct_to_template
#from django.views.generic.simple import redirect_to

from zinnia.sitemaps import TagSitemap
from zinnia.sitemaps import EntrySitemap
from zinnia.sitemaps import CategorySitemap
from zinnia.sitemaps import AuthorSitemap



admin.autodiscover()

sitemaps = {
    'tags':         TagSitemap,
    'blog':         EntrySitemap,
    'authors':      AuthorSitemap,
    'categories':   CategorySitemap,
}

urlpatterns = patterns(
    r'',

    url(r'^i18n/',      include('django.conf.urls.i18n')),

    url(r'^admin/filebrowser/', include('filebrowser.urls')),
    url(r'^admin/',     include( admin.site.urls )),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^weblog/',    include('zinnia.urls')),
    url(r'^comments/',  include('django.contrib.comments.urls')),
    url(r'',            include('contenidos.urls')),
)


# Un par de casos especiales a estudiar:
#urlpatterns += patterns(
#    r'',
#    (r'^favicon\.ico$', redirect_to, {'url': settings.STATIC_URL + 'favicon.ico'}),
#    (r'^robots\.txt$', direct_to_template, {'template': 'robots.txt', 'mimetype': 'text/plain'}),
#)


urlpatterns += patterns('django.contrib.sitemaps.views',
    url(r'^sitemap.xml$',                   'index',    {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$',  'sitemap',  {'sitemaps': sitemaps}),
)


# Formulario de contacto:
# ~~~~~~~~~~~~~~~~~~~~~~
urlpatterns += patterns(
    '',
    url(r'^contact/', include('django_contactme.urls')),
)

if 'tinymce' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        (r'^tinymce/', include('tinymce.urls')),
    )


if settings.DEBUG and not settings.PRODUCCION:
    # Desarrollo
    urlpatterns += patterns(r'',
		url(r'^html/$', TemplateView.as_view(template_name="provisional.html"), name="p"),
        url(r'^html/b$', TemplateView.as_view(template_name='base.html'), name="b"),
        url(r'^html/b1$', TemplateView.as_view(template_name='base_1col.html'), name="b1"),
        url(r'^html/b2$', TemplateView.as_view(template_name='base_2col.html'), name="b2"),
        url(r'^html/b22$', TemplateView.as_view(template_name='base_2col2.html'), name="b22"),
        url(r'^html/b3$', TemplateView.as_view(template_name='base_3col.html'), name="b3"),
        url(r'', include('debug_toolbar_user_panel.urls')),
        url(r'', include('debug_toolbar_htmltidy.urls')),
    )
    urlpatterns += patterns('django.views.static',
        #url(r'^static/(.*)$',  'serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
        url(r'^media/(.*)$',  'serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
elif settings.DEBUG and settings.PRODUCCION:
    # Beta
    pass
else:
    # Producción
    pass

# ESTA DEBE SER LA ULTIMA PUES PILLA TODO LO QUE NO PILLAN LAS DEMAS
urlpatterns += patterns(r'',
    url(r'',            include('flatpages_i18n.urls')),
)









# from django.conf import settings
# if settings.DEBUG and not settings.PRODUCCION:
#    # FIXME Esto es lo documentado, pero no sirve media
#    #from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#    #urlpatterns += staticfiles_urlpatterns()
#    print "MEDIA %s" % settings.MEDIA_ROOT
#    print "STATIC %s" % settings.STATIC_ROOT
#    urlpatterns += patterns('django.views.static',
#        url(r'^static/(.*)$',  'serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
#        url(r'^media/(.*)$',  'serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
#    )

