#-*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from contenidos.views import Calendario, EventoView

urlpatterns = patterns('',
    url(r'calendario/(?P<year>\d+)/(?P<month>\d+)$', Calendario.as_view(), name='calendario'),
    url(r'evento/(?P<pk>\d+)$', EventoView.as_view(), name='evento_view'),
)