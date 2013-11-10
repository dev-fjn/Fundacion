#-*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from contenidos.views import Calendario, EventoView, Libros, Documentos, BusquedaGeneral, CitasDe, CitasSobre
from contenidos.models import TIPO

urlpatterns = patterns('',
	url(r'calendario/(?P<year>\d+)/(?P<month>\d+)/only$', Calendario.as_view(), {'only': True}, name='calendario_only'),
	url(r'calendario/(?P<year>\d+)/(?P<month>\d+)$', Calendario.as_view(), name='calendario'),
	url(r'calendario/$', Calendario.as_view(), name='calendario'),
	url(r'libros/$', Libros.as_view(), name="libros"),
	url(r'recursos_audiovisuales/$', Documentos.as_view(), {'tipo': TIPO.RECURSOS_AUDIOVISUALES}, name="recursos_audiovisuales"),
	url(r'presencia_en_prensa/$', Documentos.as_view(), {'tipo': TIPO.PRESENCIA_EN_PRENSA}, name="presencia_en_prensa"),
	url(r'dossieres_de_prensa/$', Documentos.as_view(), {'tipo': TIPO.DOSSIERES_DE_PRENSA}, name="dossieres_de_prensa"),
	url(r'evento/(?P<pk>\d+)$', EventoView.as_view(), name='evento_view'),
	url(r'buscar/$', BusquedaGeneral.as_view(), name='busqueda_general'),
	url(r'citas-de-juan-negrin/$', CitasDe.as_view(), name='citas_de_juan_negrin'),
	url(r'citas-sobre-juan-negrin/$', CitasSobre.as_view(), name='citas_sobre_juan_negrin'),
)

