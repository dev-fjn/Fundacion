# -*- coding: utf-8 -*-

from django.utils import timezone
from dateutil.relativedelta import relativedelta
import calendar
import datetime

def inicio_fin_mes(meses_adelante): # acepta negativos tb
	now = timezone.now() + relativedelta(months=int(meses_adelante))
	start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
	end = start + relativedelta(months=1) - datetime.timedelta(seconds=1)
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

