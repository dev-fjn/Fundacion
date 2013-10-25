# -*- coding: utf-8 -*-

from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from models import Video, Imagen

class VideoAdmin(TranslationAdmin):
	list_display = ['titulo', 'flv_url', 'mp4_url']

class ImagenAdmin(TranslationAdmin):
	list_display = ['titulo']

admin.site.register(Imagen, ImagenAdmin)
admin.site.register(Video, VideoAdmin)

