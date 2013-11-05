# -*- coding: utf-8 -*-

from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from models import *

class VideoAdmin(TranslationAdmin):
	list_display = ['titulo', 'flv', 'mp4']

class ImagenAdmin(TranslationAdmin):
	list_display = ['titulo']

class FechaEventoInline(admin.StackedInline):
    model = FechaEvento
    extra = 1

class EventoAdmin(admin.ModelAdmin):
	list_display = ['titulo', 'fechas']
	inlines = [FechaEventoInline, ]

	def fechas(self, obj):
		return ", ".join([fecha.simple() for fecha in obj.fechaevento_set.all()]) 

class LibroAdmin(admin.ModelAdmin):
	list_display = ['titulo', 'autor', 'fecha', 'isbn']
	search_fields = ['titulo', 'autor', 'isbn']
	date_hierarchy = 'fecha'

class UrlInline(admin.TabularInline):
	model = Url
	extra = 0

class PdfInline(admin.TabularInline):
	model = Pdf
	extra = 0

class DocumentoAdmin(admin.ModelAdmin):
	list_display = ['titulo', 'tipo', 'adjuntos_']
	list_filter = ['tipo']
	inlines = [UrlInline, PdfInline]

	def adjuntos_(self, obj):
		return "<br />".join([u"%s" % (i, ) for i in obj.adjuntos()])
	adjuntos_.allow_tags = True


admin.site.register(Imagen, ImagenAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Libro, LibroAdmin)
admin.site.register(Documento, DocumentoAdmin)
