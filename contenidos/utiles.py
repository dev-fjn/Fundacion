# -*- coding: utf-8 -*-

from django.utils import timezone
import calendar
import datetime

def inicio_fin_mes(meses_atras):
	month = int(meses_atras)
	now = timezone.now()
	# mes actual (del 1 al corriente)
	start, end = now.replace(day=1), now
	# ir meses atras (del 1 al ultimo)
	for i in range(month):
		end = start-datetime.timedelta(days=1)
		start = end.replace(day=1)
	return start, end

def calendario_por_meses(start, end, diccionario):
	# obtenemos las semanas+dias de un calendario del mes
	c = calendar.Calendar(calendar.MONDAY)
	weeks = c.monthdatescalendar(start.year, start.month)
	# introducimos la clasificacion en las semanas+dias
	semanas = []
	for week in weeks:
		semana = []
		for day in week:
			semana.append( (day, (diccionario[day] if day in diccionario else [])) )
		semanas.append(semana)
	return semanas

