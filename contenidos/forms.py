#-*- coding: utf-8 -*-

from django import forms

class BusquedaComplejaForm(forms.Form):
	encontrar = forms.CharField(label=u'¿Qué quieres buscar?')
