# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.


def _siguiente_orden():
	m = Imagen.objects.aggregate(models.Max("orden"))["orden__max"]
	return 1 if not m else m+1

class Imagen(models.Model):
	titulo = models.CharField(max_length=250)
	orden = models.IntegerField(default=_siguiente_orden)
	imagen = models.ImageField(upload_to="imagenes")

	def __unicode__(self):
		return self.titulo

	class Meta:
		verbose_name = u'imagen'
		verbose_name_plural = u'imágenes'
		ordering = ('orden', )

class Video(models.Model):
	titulo = models.CharField(max_length=250)
	flv_url = models.CharField(max_length=200, blank=True)
	mp4_url = models.CharField(max_length=200, blank=True)

	class Meta:
		verbose_name = u'vídeo'
		verbose_name_plural = u'vídeos'

