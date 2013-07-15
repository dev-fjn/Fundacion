# -*- coding: utf-8 -*-

'''Vistas del index.html del proyecto.'''

# from django.http import HttpResponse

from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime, timedelta    # django_contactme
from django_contactme import signals        # django_contactme

def home(request):
    '''Ejemplo de vista básica.'''

    context = {'listado': [],}

    return render_to_response('portada/index.html', context, RequestContext(request))

# def plantilla_integrada(request):
#     html = "<html><head><title></title></head><body><p>Ejemplo de plantilla integrada.</p></body></html>"
#     return HttpResponse(html)

def check_submit_date_is_within_last_7days(
    sender,
    data,
    request,
    **kwargs):
    '''Señal (signal) para ver si es más antiguo que una semana.'''
    plus7days = timedelta(days=7)
    if data["submit_date"] + plus7days < datetime.now():
        return False

signals.confirmation_received.connect(check_submit_date_is_within_last_7days)

