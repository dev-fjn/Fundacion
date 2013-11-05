# -*- coding: utf-8 -*-

from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from models import Video, Imagen, Evento, FechaEvento, Libro

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

admin.site.register(Imagen, ImagenAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Libro, LibroAdmin)


