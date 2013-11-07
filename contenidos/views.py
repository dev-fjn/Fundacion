#-*- coding: utf-8 -*-

from contenidos.forms import BusquedaComplejaForm
from contenidos.models import Evento, FechaEvento, Libro, Documento, TIPO
from contenidos.utiles import inicio_fin_mes, calendario_por_meses
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView, FormView
from flatpages_i18n.models import FlatPage_i18n
import calendar
import datetime

class Calendario(TemplateView):
	def get_template_names(self):
		if 'only' in self.kwargs:
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
				'only': self.kwargs.get('only'),
				'hoy': now,
				'start': start,
				'semanas': semanas,
				'prev': start - datetime.timedelta(days=1),
				'next': end + datetime.timedelta(days=1),
				'object_list': FechaEvento.objects.filter(fecha__gte=start, fecha__lte=end),
			})
		return context

class EventoView(DetailView):
	model = Evento

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(EventoView, self).get_context_data(**kwargs)
		return context

class Libros(ListView):
	model = Libro
	paginate_by = 2

class Documentos(ListView):
	model = Documento
	paginate_by = 2

	def get_queryset(self):
		qs = super(Documentos, self).get_queryset()
		if 'tipo' in self.kwargs:
			qs = qs.filter(tipo=self.kwargs['tipo'])
		return qs

	def get_context_data(self, **kwargs):
		context = super(Documentos, self).get_context_data(**kwargs)
		tipo = self.kwargs.get('tipo')
		context["tipo"] = TIPO.DICT[tipo] if tipo in TIPO.DICT else "(Ninguno)"
		context["base_tipo"] = TIPO.BASES_HORMIGAS[tipo] if tipo in TIPO.BASES_HORMIGAS else "(Ninguno)"
		return context

class BusquedaLibros(FormView):
	form_class = BusquedaComplejaForm
	template_name = "contenidos/busqueda_libros.html"
	success_url = "."

	def form_valid(self, form):
		return super(BusquedaLibros, self).form_valid(form)

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
				'libros_list': busqueda_exhaustiva(Libro, query, 'titulo', 'autor', 'resumen'),
			})
		return context

