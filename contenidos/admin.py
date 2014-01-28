# -*- coding: utf-8 -*-

from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from tinymce.widgets import TinyMCE

from models import *

TINYMCE_COMMON = {
    # http://www.tinymce.com/wiki.php/Configuration3x
    'theme': 'advanced',
    'entity_encoding': 'raw',
    # ojo, que hay que poner por cada tag, los atributos que se dejan! por ejemplo  a[href|target|title]
    #'extended_valid_elements': 'figure[corregir|esto],caption[y|esto]', ... casi mejor ponerlo todo
    'valid_elements': '*[*]',
}

TINYMCE_SIMPLE = {
    'theme_advanced_buttons1': "bold,italic,underline,strikethrough,|,bullist,numlist,|,cut,copy,paste,|,undo,redo,|,link,unlink,image,|,cleanup,removeformat,code",
}

TINYMCE_ADVANCED = {
}


FORMFIELD_TINYMCE_SIMPLE = {
    models.TextField: {'widget': TinyMCE(attrs={'cols': 10, 'cols': 80}, mce_attrs=dict(TINYMCE_COMMON.items() + TINYMCE_SIMPLE.items()))},
}

FORMFIELD_TINYMCE_AVANZADO = {
    models.TextField: {'widget': TinyMCE(attrs={'cols': 10, 'cols': 80}, mce_attrs=dict(TINYMCE_COMMON.items() + TINYMCE_ADVANCED.items()))},
}

class CarruselAdmin(TranslationAdmin):
    list_display = ['titulo', 'orden', 'filename']

class FechaEventoInline(admin.StackedInline):
    model = FechaEvento
    extra = 1

class EventoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'fechas']
    inlines = [FechaEventoInline, ]
    formfield_overrides = FORMFIELD_TINYMCE_SIMPLE

    def fechas(self, obj):
        return ", ".join([fecha.simple() for fecha in obj.fechaevento_set.all()]) 


class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'fecha', 'isbn']
    search_fields = ['titulo', 'autor', 'isbn']
    date_hierarchy = 'fecha'
    formfield_overrides = FORMFIELD_TINYMCE_SIMPLE

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
    formfield_overrides = FORMFIELD_TINYMCE_SIMPLE

    def adjuntos_(self, obj):
        return "<br />".join([u"%s" % (i, ) for i in obj.adjuntos()])
    adjuntos_.allow_tags = True

class CitasDeAdmin(admin.ModelAdmin):
    list_display = ['contenido', 'fecha']
    formfield_overrides = FORMFIELD_TINYMCE_SIMPLE

class CitasSobreAdmin(admin.ModelAdmin):
    list_display = ['contenido', 'autor', 'fecha']
    formfield_overrides = FORMFIELD_TINYMCE_SIMPLE

class PresenciaAdmin(admin.ModelAdmin):
    list_display = ['denominacion', 'lugar', ]
    formfield_overrides = FORMFIELD_TINYMCE_AVANZADO

admin.site.register(Carrusel, CarruselAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Libro, LibroAdmin)
admin.site.register(Categoria, CategoriaDocumentoAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(CitaDe, CitasDeAdmin)
admin.site.register(CitaSobre, CitasSobreAdmin)
admin.site.register(Presencia, PresenciaAdmin)


# FIXME
# 
# Esto es un poco chapucero ponerlo aqui dentro. Lo ideal seria hacer una
# app completa de flatpages heredando o rehaciendo la original. Pero eso
# implica tumbarse todos los datos existentes y recrear las tablas. Cuando
# nos independicemos de flatpages, quitar esto de aqui.
# 
# Ojito: a esto puede afectar el orden en el que se cargue en el installed_apps.

from flatpages_i18n.models import FlatPage_i18n
from flatpages_i18n.admin import FlatPageAdmin

class MyFlatPageAdmin(FlatPageAdmin):
    formfield_overrides = FORMFIELD_TINYMCE_SIMPLE

try:
    admin.site.unregister(FlatPage_i18n)
except admin.sites.NotRegistered:
    pass # por alguna razon hace este fallo de vez en cuando

admin.site.register(FlatPage_i18n, MyFlatPageAdmin)

