#-*- coding: utf-8 -*-

from contenidos.models import Evento, FechaEvento, Libro
from contenidos.utiles import inicio_fin_mes, calendario_por_meses
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView
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

