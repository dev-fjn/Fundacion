# -*- coding: utf-8 -*-

from django.db import models
from filebrowser.fields import FileBrowseField

# Create your models here.


def _siguiente_orden():
	m = Imagen.objects.aggregate(models.Max("orden"))["orden__max"]
	return 1 if not m else m+1

class Imagen(models.Model):
	titulo = models.CharField(max_length=250)
	orden = models.IntegerField(default=_siguiente_orden)
	imagen = FileBrowseField("Imagen", max_length=200, directory="imagenes")

	def __unicode__(self):
		return self.titulo

	class Meta:
		verbose_name = u'imagen'
		verbose_name_plural = u'imágenes'
		ordering = ('orden', )

class Video(models.Model):
	titulo = models.CharField(max_length=250)
	flv = FileBrowseField("FLV", max_length=200, extensions=[".flv",], directory="videos", blank=True, null=True)
	mp4 = FileBrowseField("MP4", max_length=200, extensions=[".mp4",], directory="videos", blank=True, null=True)

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

	@staticmethod
	def datos_para_calendario(start, end):
		qs = FechaEvento.objects.filter(fecha__gte=start, fecha__lte=end)
		# clasificamos los resultados por dias
		v = {}
		for fe in qs:
			dmy = fe.fecha
			if not dmy in v:
				v[dmy] = []
			v[dmy].append(fe.evento)
		return v

class FechaEvento(models.Model):
	evento = models.ForeignKey(Evento)
	fecha = models.DateField()
	hora_inicio = models.TimeField()
	hora_final = models.TimeField()

	def simple(self):
		return u"%s %s...%s" % (self.fecha, self.hora_inicio, self.hora_final, )

	def __unicode__(self):
		return u"%s %s-%s (%s)" % (self.fecha, self.hora_inicio, self.hora_final, self.evento)


class Libro(models.Model):
	titulo = models.CharField(max_length=250)
	autor = models.CharField(max_length=250)
	isbn = models.CharField(max_length=13)
	fecha = models.DateField()
	precio = models.FloatField()
	miniatura = models.ImageField(upload_to="libros")
	url = models.URLField(blank=True, null=True)
	resumen = models.TextField()

	def __unicode__(self):
		return u"%s (%s)" % (self.titulo, self.autor)

class TIPO:
	RECURSOS_AUDIOVISUALES = 1
	PRESENCIA_EN_PRENSA = 2
	DOSSIERES_DE_PRENSA = 3
	CHOICES = (
		(RECURSOS_AUDIOVISUALES, 'Recursos Audiovisuales'),
		(PRESENCIA_EN_PRENSA, 'Presencia en Prensa'),
		(DOSSIERES_DE_PRENSA, 'Dossieres de Prensa'),
		)
	DICT = dict(CHOICES)

class Documento(models.Model):
	tipo = models.IntegerField(choices=TIPO.CHOICES)
	titulo = models.CharField(max_length=250)
	descripcion = models.TextField()

	def adjuntos(self):
		l = list(self.urladjunto_set.all())
		l += list(self.pdfadjunto_set.all())
		l += list(self.videoadjunto_set.all())
	        l += list(self.audioadjunto_set.all())
		return sorted(l, key=lambda x: x.titulo)

class Adjunto(models.Model):
	documento = models.ForeignKey(Documento)
	titulo = models.CharField(max_length=250)

	def template(self):
		return "contenidos/_%s.html" % (self.__class__.__name__.lower(), )

	def __unicode__(self):
		return u"%s: %s" % (self.__class__.__name__.upper(), self.titulo)
	
	class Meta:
		abstract = True

class UrlAdjunto(Adjunto):
    url = models.URLField()

    class Meta:
        verbose_name = u'URL adjunta'
        verbose_name_plural = u'URLs adjuntas'

class PdfAdjunto(Adjunto):
    pdf = FileBrowseField("pdf", max_length=200, extensions=[".pdf",], directory="documentos", blank=True, null=True)

    class Meta:
        verbose_name = u'PDF adjunto'
        verbose_name_plural = u'PDFs adjuntos'

class VideoAdjunto(Adjunto):
    video = FileBrowseField("video", max_length=200, extensions=[".flv", ".mp4",], directory="documentos", blank=True, null=True)

    class Meta:
        verbose_name = u'Vídeo adjunto'
        verbose_name_plural = u'Vídeos adjuntos'

class AudioAdjunto(Adjunto):
    audio = FileBrowseField("audio", max_length=200, extensions=[".mp3", ".ogg",], directory="documentos", blank=True, null=True)

    class Meta:
        verbose_name = u'Audio adjunto'
        verbose_name_plural = u'Audios adjuntos'

