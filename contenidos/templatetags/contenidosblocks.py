from django import template
register = template.Library()

from contenidos.models import Imagen, Video, Evento, FechaEvento
from contenidos.utiles import inicio_fin_mes, calendario_por_meses
from django.conf import settings
from django.utils import timezone
import datetime

@register.inclusion_tag('contenidos/_imagenes.html')
def imagenes():
    imagenes = Imagen.objects.all()
    return {'MEDIA_URL': settings.MEDIA_URL, 'imagenes': imagenes}

@register.inclusion_tag('contenidos/_videos.html')
def videos():
    return {'MEDIA_URL': settings.MEDIA_URL, "videos": Video.objects.all() }

@register.inclusion_tag('contenidos/_proximos_eventos.html')
def proximos_eventos():
	start = timezone.now()
	end = start+datetime.timedelta(days=60)
	# buscar eventos en rango
	qs = FechaEvento.objects.filter(fecha__gte=start, fecha__lte=end)
	return {'object_list': qs}

from contenidos.utiles import calendario_por_meses

@register.inclusion_tag('contenidos/_calendario_eventos.html')
def calendario_eventos(meses_atras):
	start, end = inicio_fin_mes(meses_atras)
	diccionario = Evento.datos_para_calendario(start, end)
	semanas = calendario_por_meses(start, end, diccionario)
	return {
			'only': True,
			'hoy': timezone.now(), 
			'start': start, 
			'semanas': semanas, 
			'prev': start-datetime.timedelta(days=1), 
			'next': end+datetime.timedelta(days=1),
		}

# ESTO ES OTRA FORMA DE HACER LO MSIMO QUE ARRIBA, PERO EN ESTE CASO
# TODA LA PRESENTACION SE HACE DESDE PYTHON. LO DEJO A MODO DE EJEMPLO
# UNOS DIAS ANTES DE BORRARLO, PUES PARECE MEJOR HACER LA PRESENTACION
# EN TEMPLATE.
#
#class MyHTMLCalendar(calendar.HTMLCalendar):
#	def formatmonth(self, year, month, v):
#		self.year = year
#		self.month = month
#		self.v = v
#		return super(MyHTMLCalendar, self).formatmonth(year, month)
#
#	def formatday(self, day, weekday):
#		if day == 0:
#			out = '<td class="noday">&nbsp;</td>' # day outside month
#		else:
#			out = '<td class="%s">%d' % (self.cssclasses[weekday], day)
#			dmy = datetime.date(self.year, self.month, day)
#			if dmy in self.v:
#				for evento in self.v[dmy]:
#					out += '<br/><a href="%s">%s</a>' % (evento.id, evento)
#			out += '</td>'
#		return out
#
#@register.inclusion_tag('contenidos/_none.html')
#def calendario_eventos2(month):
#	month = int(month)
#	now = timezone.now()
#	# mes actual
#	start, end = now.replace(day=1), now
#	# ir meses atras
#	for i in range(month):
#		end = start-datetime.timedelta(days=1)
#		start = end.replace(day=1)
#	# buscar eventos en rango
#	qs = FechaEvento.objects.filter(fecha__gte=start, fecha__lte=end)
#	v = {}
#	for fe in qs:
#		dmy = fe.fecha
#		if not dmy in v:
#			v[dmy] = []
#		v[dmy].append(fe.evento)
#	c = MyHTMLCalendar(calendar.MONDAY)
#	return {'object': c.formatmonth(start.year, start.month, v)}
#
# FIN BLOQUE ANTERIOR

@register.inclusion_tag('contenidos/_proximos_eventos.html')
def proximos_eventos():
	start = timezone.now()
	end = start+datetime.timedelta(days=60)
	# buscar eventos en rango
	qs = FechaEvento.objects.filter(fecha__gte=start, fecha__lte=end)
	return {'object_list': qs}

