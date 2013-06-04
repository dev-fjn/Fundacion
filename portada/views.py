# -*- coding: utf-8 -*-

'''Vistas del index.html del proyecto.'''

# from django.http import HttpResponse

from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    '''Ejemplo de vista básica.'''

    context = {'listado': [],}

    return render_to_response('portada/index.html', context, RequestContext(request))

# def plantilla_integrada(request):
#     html = "<html><head><title></title></head><body><p>Ejemplo de plantilla integrada.</p></body></html>"
#     return HttpResponse(html)
