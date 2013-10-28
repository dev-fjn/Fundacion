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

class Evento(models.Model):
	titulo = models.CharField(max_length=250)
	resumen = models.TextField()
	fecha_y_lugar = models.TextField()
	imagen = models.ImageField(upload_to="eventos/imagenes")
	pdf = models.FileField(upload_to="eventos/pdf", blank=True, null=True)

	def __unicode__(self):
		return u"%s" % (self.titulo, )

class LugarEvento(models.Model):
	evento = models.ForeignKey(Evento)
	latitud = models.FloatField()
	longitud = models.FloatField()

	def __unicode__(self):
		return u"%.4f,%.4f (%s)" % (self.latitud, self.longitud, self.evento)

class FechaEvento(models.Model):
	evento = models.ForeignKey(Evento)
	fecha = models.DateField()
	hora_inicio = models.TimeField()
	hora_final = models.TimeField()

	def simple(self):
		return u"%s %s...%s" % (self.fecha, self.hora_inicio, self.hora_final, )

	def __unicode__(self):
		return u"%s %s-%s (%s)" % (self.fecha, self.hora_inicio, self.hora_final, self.evento)

