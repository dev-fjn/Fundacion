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

class UrlAdjuntoInline(admin.TabularInline):
    model = UrlAdjunto
    extra = 0

class FicheroAdjuntoInline(admin.TabularInline):
    model = FicheroAdjunto
    extra = 0

class CategoriaDocumentoAdmin(admin.ModelAdmin):
    pass

class AutorAdmin(admin.ModelAdmin):
    pass

class DocumentoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'autor', 'adjuntos_']
    list_filter = ['categoria__tipo', 'categoria', 'autor']
    inlines = [UrlAdjuntoInline, FicheroAdjuntoInline]
    prepopulated_fields = { "slug": ("titulo",) }

    def adjuntos_(self, obj):
        return "<br />".join([u"%s" % (i, ) for i in obj.adjuntos()])
    adjuntos_.allow_tags = True

class CitasDeAdmin(admin.ModelAdmin):
    list_display = ['contenido', 'fecha']

class CitasSobreAdmin(admin.ModelAdmin):
    list_display = ['contenido', 'autor', 'fecha']

class PresenciaAdmin(admin.ModelAdmin):
    list_display = ['denominacion', 'lugar', ]

admin.site.register(Imagen, ImagenAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Libro, LibroAdmin)
admin.site.register(Categoria, CategoriaDocumentoAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(CitaDe, CitasDeAdmin)
admin.site.register(CitaSobre, CitasSobreAdmin)
admin.site.register(Presencia, PresenciaAdmin)
