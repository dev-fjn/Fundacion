#-*- coding: utf-8 -*-

from contenidos.models import Evento, FechaEvento, Libro, Documento, TIPO
from contenidos.utiles import calendario_por_meses
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView
from flatpages_i18n.models import FlatPage_i18n
import calendar
import datetime

class Calendario(TemplateView):
    only = False

    def get_template_names(self):
        if self.only:
            return "contenidos/_calendario_eventos.html"
        else:
            return "contenidos/calendario.html"

    def get_context_data(self, **kwargs):
        context = super(Calendario, self).get_context_data(**kwargs)
        now = timezone.now()
        if not 'year' in kwargs or not 'month' in kwargs:
            year, month = now.year, now.month
        else:
            year, month = int(kwargs.get('year')), int(kwargs.get('month'))
        start = datetime.date(year, month, 1)
        dsemana, dultimo = calendar.monthrange(year, month)
        end = start + datetime.timedelta(days=dultimo-1)
        diccionario = Evento.datos_para_calendario(start, end)
        semanas = calendario_por_meses(start, end, diccionario)
        context.update({
                'only': self.only,
                'hoy': now,
                'start': start,
                'semanas': semanas,
                'prev': start - datetime.timedelta(days=1),
                'next': end + datetime.timedelta(days=1),
                'object_list': FechaEvento.objects.filter(fecha__gte=start, fecha__lte=end),
            })
        return context

class LibrosBase(object):
    externos = None

    CONTEXT_PROPIOS = {
            'url': "catalogo_de_publicaciones",
            'page_title': u"Catálogo de publicaciones",
            'page_parent': u"Fondos y Recursos Documentales",
            'verbose_name': u"publicación",
            'verbose_name_plural': u"publicaciones",
        }

    CONTEXT_EXTERNOS = {
            'url': 'bibliografia',
            'page_title': u"Bibliografía",
            'page_parent': u"Juan Negrín",
            'verbose_name': u"recurso bibliográfico",
            'verbose_name_plural': u"recursos bibliográficos",
        }

    @property
    def extra_context(self):
        return self.CONTEXT_EXTERNOS if self.externos else self.CONTEXT_PROPIOS
        
    def get_queryset(self):
        return super(LibrosBase, self).get_queryset().filter(precio__isnull = self.externos)

    def get_context_data(self, **kwargs):
        context = super(LibrosBase, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        autores = set(Libro.objects.values_list('autor', flat=True))
        isbns = set(Libro.objects.filter(isbn__isnull=False).values_list('isbn', flat=True))
        titulos = set(Libro.objects.values_list('titulo', flat=True))
        context['datalist'] = autores.union(isbns, titulos)
        return context

    def dispatch(self, *args, **kwargs):
        # Esto es para la vista del buscador. El resto de urls.py tienen "externos" puesto.
        if self.externos is None:
            self.externos = self.kwargs.get('tipo') == self.CONTEXT_EXTERNOS['url']
        return super(LibrosBase, self).dispatch(*args, **kwargs)

class LibroDetalle(LibrosBase, DetailView):
    model = Libro

class Libros(LibrosBase, ListView):
    model = Libro
    paginate_by = settings.CONTENIDOS_PAGINADOR_MAX

    
    def dispatch(self, *args, **kwargs):
        # si nos pasan rollos por GET, nos los quitamos de encima y redirigimos por URL
        query = self.request.GET.get('query', '')
        if query:
            return redirect(reverse('libro_busqueda', kwargs=dict(tipo = self.extra_context['url'], query = query)))
        return super(Libros, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super(Libros, self).get_queryset()
        self.valor = self.kwargs.get("query", "").strip() or self.request.GET.get("query", "")
        if self.valor:
            qs = qs.filter( Q(titulo__icontains=self.valor) | Q(autor__icontains=self.valor) | Q(resumen__icontains=self.valor) | Q(isbn__icontains=self.valor))
        self.count = qs.count()
        return qs

    def get_context_data(self, **kwargs):
        context = super(Libros, self).get_context_data(**kwargs)
        context['query'] = self.valor
        context['count'] = self.count
        return context

class DocumentosBase(object):
    tipo = None

    def get_queryset(self):
        qs = super(DocumentosBase, self).get_queryset()
        if self.tipo:
            qs = qs.filter(categoria__tipo=self.tipo)
        return qs

    def get_context_data(self, **kwargs):
        context = super(DocumentosBase, self).get_context_data(**kwargs)
        context["tipo"] = TIPO.DICT[self.tipo] if self.tipo in TIPO.DICT else "(Ninguno)"
        context["base_tipo"] = TIPO.BASES_HORMIGAS[self.tipo] if self.tipo in TIPO.BASES_HORMIGAS else "(Ninguno)"
        return context

class DocumentoDetalle(DocumentosBase, DetailView):
    model = Documento

class Documentos(DocumentosBase, ListView):
    model = Documento
    paginate_by = settings.CONTENIDOS_PAGINADOR_MAX

    def get_queryset(self):
        qs = super(Documentos, self).get_queryset()
        self.query = self.request.GET.get('query', '').strip()
        if self.query:
            qs = qs.filter(Q(titulo__icontains=self.query)|Q(descripcion__icontains=self.query))
        self.count = qs.count()
        return qs

    def get_context_data(self, **kwargs):
        context = super(Documentos, self).get_context_data(**kwargs)
        context["query"] = self.query
        context["count"] = self.count
        return context

class BusquedaGeneral(TemplateView):
    template_name = "contenidos/busqueda_general.html"

    def get_context_data(self, **kwargs):
        context = super(BusquedaGeneral, self).get_context_data(**kwargs)
        query = self.request.GET.get('query', '').strip()
        context['query'] = query

        if len(query) == 0:
            return context

        if len(query) < 3:
            context['error'] = "Necesita buscar un mínimo de 3 caracteres"
            return context

        def busqueda_exhaustiva(klz, query, *args):
            q = Q()
            for arg in args:
                filtro = {"%s__icontains" % arg: query}
                q |= Q(**filtro)
            return klz.objects.filter(q)

        context.update({
                'eventos_list': busqueda_exhaustiva(Evento, query, 'titulo'),
                'paginas_list': busqueda_exhaustiva(FlatPage_i18n, query, 'title', 'content'),
                'libros_list': busqueda_exhaustiva(Libro, query, 'titulo', 'autor', 'resumen', 'isbn'),
            })
        return context

