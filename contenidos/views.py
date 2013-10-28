#-*- coding: utf-8 -*-

from contenidos.models import Evento, FechaEvento
from contenidos.utiles import inicio_fin_mes, calendario_por_meses
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
import calendar
import datetime

class Calendario(TemplateView):
	template_name = "contenidos/calendario.html"

	def get_context_data(self, **kwargs):
		context = super(Calendario, self).get_context_data(**kwargs)
		if not 'year' in kwargs or not 'month' in kwargs:
			return context
		year, month = int(kwargs.get('year')), int(kwargs.get('month'))
		start = datetime.date(year, month, 1)
		dsemana, dultimo = calendar.monthrange(year, month)
		end = start + datetime.timedelta(days=dultimo-1)
		diccionario = Evento.datos_para_calendario(start, end)
		semanas = calendario_por_meses(start, end, diccionario)
		context.update({
				'hoy': timezone.now(),
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

