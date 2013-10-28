# -*- coding: utf-8 -*-

from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from models import Video, Imagen, Evento, LugarEvento, FechaEvento

class VideoAdmin(TranslationAdmin):
	list_display = ['titulo', 'flv_url', 'mp4_url']

class ImagenAdmin(TranslationAdmin):
	list_display = ['titulo']

class LugarEventoInline(admin.StackedInline):
    model = LugarEvento
    extra = 1

class FechaEventoInline(admin.StackedInline):
    model = FechaEvento
    extra = 1

class EventoAdmin(admin.ModelAdmin):
	list_display = ['titulo', 'fechas']
	inlines = [LugarEventoInline, FechaEventoInline, ]
	def fechas(self, obj):
		return ", ".join([fecha.simple() for fecha in obj.fechaevento_set.all()]) 

admin.site.register(Imagen, ImagenAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Evento, EventoAdmin)

