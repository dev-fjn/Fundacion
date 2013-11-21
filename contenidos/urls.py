#-*- coding: utf-8 -*-

from contenidos.models import CitaDe, CitaSobre, Evento, Presencia
from contenidos.models import TIPO
from contenidos.views import Calendario, Libros, LibroDetalle, Documentos, DocumentoDetalle, BusquedaGeneral
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, ListView, DetailView

urlpatterns = patterns('',
    url(r'bibliografia/$', Libros.as_view(externos=True), name="bibliografia"),
    url(r'bibliografia/(?P<pk>\d+)$', LibroDetalle.as_view(externos=True), name="libro_detalle"),
    url(r'buscador/$', BusquedaGeneral.as_view(), name='busqueda_general'),
    url(r'busqueda/(?P<tipo>\w+)/(?P<query>.+)$', Libros.as_view(), name="libro_busqueda"),
    url(r'calendario/$', Calendario.as_view(), name='calendario'),
    url(r'calendario/(?P<year>\d+)/(?P<month>\d+)$', Calendario.as_view(), name='calendario'),
    url(r'calendario/(?P<year>\d+)/(?P<month>\d+)/only$', Calendario.as_view(only=True), name='calendario_only'),
    url(r'catalogo_de_publicaciones/$', Libros.as_view(externos=False), name="catalogo_de_publicaciones"),
    url(r'catalogo_de_publicaciones/(?P<pk>\d+)$', LibroDetalle.as_view(externos=False), name="publicacion_detalle"),
    url(r'citas-de-juan-negrin/$', ListView.as_view(model=CitaDe), name='citas_de_juan_negrin'),
    url(r'citas-sobre-juan-negrin/$', ListView.as_view(model=CitaSobre), name='citas_sobre_juan_negrin'),
    url(r'dossieres_de_prensa/$', Documentos.as_view(tipo=TIPO.DOSSIERES_DE_PRENSA), name="dossieres_de_prensa"),
    url(r'dossieres_de_prensa/(?P<pk>\d+)$', DocumentoDetalle.as_view(tipo=TIPO.DOSSIERES_DE_PRENSA), name="dossier_de_prensa_detalle"),
    url(r'evento/(?P<pk>\d+)$', DetailView.as_view(model=Evento), name='evento_view'),
    url(r'presencia_en_prensa/$', Documentos.as_view(tipo=TIPO.PRESENCIA_EN_PRENSA), name="presencia_en_prensa"),
    url(r'presencia_en_prensa/(?P<pk>\d+)$', DocumentoDetalle.as_view(tipo=TIPO.PRESENCIA_EN_PRENSA), name="presencia_en_prensa_detalle"),
    url(r'presencia/$', ListView.as_view(model=Presencia), name="presencia"),
    url(r'recursos_audiovisuales/$', Documentos.as_view(tipo=TIPO.RECURSOS_AUDIOVISUALES), name="recursos_audiovisuales"),
    url(r'recursos_audiovisuales/(?P<pk>\d+)$', DocumentoDetalle.as_view(tipo=TIPO.RECURSOS_AUDIOVISUALES), name="recurso_audiovisual_detalle"),
    url(r'^$', TemplateView.as_view(template_name="contenidos/home.html"), name='home'),
)

