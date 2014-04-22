# -*- coding: utf-8 -*-

from contenidos.models import CitaDe, CitaSobre, Evento, Presencia
from contenidos.models import TIPO
from contenidos.views import Home, Calendario, EventoDay, Libros, \
    LibroDetalle, Documentos, DocumentoDetalle, BusquedaGeneral
from django.conf.urls import patterns, url
from django.conf import settings
from django.views.generic import ListView, DetailView

urlpatterns = patterns(
    '',
    url(r'bibliografia/$',
        Libros.as_view(externos=True),
        name="bibliografia"),
    url(r'bibliografia/(?P<pk>\d+)$',
        LibroDetalle.as_view(externos=True),
        name="libro_detalle"),
    url(r'buscador/$',
        BusquedaGeneral.as_view(),
        name='busqueda_general'),
    url(r'buscador/(?P<tipo>\w+)/(?P<query>.+)$',
        BusquedaGeneral.as_view(),
        name="busqueda_general_resultados"),
    url(r'busqueda/(?P<tipo>\w+)/(?P<query>.+)$',
        Libros.as_view(),
        name="libro_busqueda"),
    url(r'calendario/(?P<year>\d+)/(?P<month>\d+)$',
        Calendario.as_view(),
        name='calendario_js'),
    url(r'catalogo_de_publicaciones/$',
        Libros.as_view(externos=False),
        name="catalogo_de_publicaciones"),
    url(r'catalogo_de_publicaciones/(?P<pk>\d+)$',
        LibroDetalle.as_view(externos=False),
        name="publicacion_detalle"),
    url(r'citas-de-juan-negrin/$',
        ListView.as_view(model=CitaDe),
        name='citas_de_juan_negrin'),
    url(r'citas-sobre-juan-negrin/$',
        ListView.as_view(model=CitaSobre),
        name='citas_sobre_juan_negrin'),
    url(r'dossieres_de_prensa/$',
        Documentos.as_view(tipo=TIPO.DOSSIERES_DE_PRENSA),
        name="dossieres_de_prensa"),
    url(r'dossieres_de_prensa/(?P<slug>[-\w]+)$',
        DocumentoDetalle.as_view(tipo=TIPO.DOSSIERES_DE_PRENSA),
        name="dossier_de_prensa_detalle"),
    url(r'evento/(?P<pk>\d+)$',
        DetailView.as_view(model=Evento),
        name='evento_view'),
    url(r'evento/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)$',
        EventoDay.as_view(),
        name='evento_day'),
    url(r'presencia_en_prensa/$',
        Documentos.as_view(tipo=TIPO.PRESENCIA_EN_PRENSA),
        name="presencia_en_prensa"),
    url(r'presencia_en_prensa/(?P<slug>[-\w]+)$',
        DocumentoDetalle.as_view(tipo=TIPO.PRESENCIA_EN_PRENSA),
        name="presencia_en_prensa_detalle"),
    url(r'presencia/$',
        ListView.as_view(model=Presencia,
                         paginate_by=settings.CONTENIDOS_PAGINADOR_MAX),
        name="presencia"),
    url(r'recursos_audiovisuales/$',
        Documentos.as_view(tipo=TIPO.RECURSOS_AUDIOVISUALES),
        name="recursos_audiovisuales"),
    url(r'recursos_audiovisuales/(?P<slug>[-\w]+)$',
        DocumentoDetalle.as_view(tipo=TIPO.RECURSOS_AUDIOVISUALES),
        name="recurso_audiovisual_detalle"),
    url(r'^$', Home.as_view(), name='home'),
)
