# -*- coding: utf-8 -*-

from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from filebrowser.fields import FileBrowseField
from zinnia.models import Category as CategoryZinnia, Entry as EntryZinnia

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
    imagen = models.ImageField(upload_to="eventos/imagenes", blank=True, null=True)
    pdf = models.FileField(upload_to="eventos/pdf", blank=True, null=True)

    def __unicode__(self):
        return u"%s" % (self.titulo, )
    
    def fecha_simple(self):
        return ", ".join([ev.simple() for ev in self.fechaevento_set.all()])

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

class TIPO:
    PONENCIAS = u'Ponencias'
    LIBRO = u'Libro'
    INFORME = u'Informe'
    BOLETIN = u'Boletín'
    CATALOGO = u'Catálogo'
    LIST = [PONENCIAS, LIBRO, INFORME, BOLETIN, CATALOGO]
    CHOICES = zip(LIST, LIST)

class Libro(models.Model):
    titulo = models.CharField(max_length=250)
    autor = models.CharField(max_length=250)
    editorial = models.CharField(max_length=250)
    tipo = models.CharField(max_length=40, choices=TIPO.CHOICES, default=TIPO.LIBRO)
    pais = models.CharField(u'país', max_length=40)# , default=u'España')
    fecha = models.DateField()
    idioma = models.CharField(max_length=40, default=u'Castellano')
    precio = models.FloatField(blank=True, null=True)
    isbn = models.CharField('ISBN', max_length=13+4, blank=True, null=True)
    miniatura = FileBrowseField("portada", max_length=200, extensions=[".jpg", ".jpeg", ".png", ".gif"], directory="bibliografia", blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    resumen = models.TextField(blank=True, null=True)

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
    BASES_HORMIGAS = {
        RECURSOS_AUDIOVISUALES: 'Fondos y Recursos Documentales',
        PRESENCIA_EN_PRENSA: 'Fondos y Recursos Documentales',
        DOSSIERES_DE_PRENSA: 'Sala de Prensa',
    }

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

class CitaDe(models.Model):
    contenido = models.TextField(help_text=u"Poner el texto que se cita")
    descripcion = models.CharField('descripción', max_length=250, help_text="Evento (y lugar) donde se realizó", default=u"Discurso")
    fecha = models.DateField(help_text="Escribir fecha exacta (o fecha de ordenación)")
    fecha_literal = models.CharField(max_length=250, blank=True, null=True, help_text="Escribir fecha a mostrar (en blanco si es exacta, escribir algo si es ambigua o no se conoce la exacta)")

    def __unicode__(self):
        return u"%s" % (self.contenido, )

    class Meta:
        verbose_name = u'cita de Juan Negrín'
        verbose_name_plural = u'citas de Juan Negrín'

class CitaSobre(models.Model):
    contenido = models.TextField(help_text=u"Poner el texto que se cita")
    autor = models.CharField(max_length=250, help_text="Autor de la cita")
    cargo = models.CharField(max_length=250, blank=True, null=True, help_text="Cargo del autor (si procede)")
    fecha = models.DateField(help_text="Escribir fecha exacta (o fecha de ordenación)")
    fecha_literal = models.CharField(max_length=250, blank=True, null=True, help_text="Escribir fecha a mostrar (en blanco si es exacta, escribir algo si es ambigua o no se conoce la exacta)")

    def __unicode__(self):
        return u"%s: %s" % (self.contenido, self.autor)

    class Meta:
        verbose_name = u'cita sobre Juan Negrín'
        verbose_name_plural = u'citas sobre Juan Negrín'

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

@receiver(post_save, sender=Evento)
def crea_blog_al_guardar_evento(sender, instance, **kwargs):
    if instance:
        e, created = EntryZinnia.objects.get_or_create(slug="evento-%d" % instance.pk)
        if created:
            print "Autocreando entrada", e, e.pk
            e.title = u"Nuevo evento: %s" % instance.titulo
            e.content = u"<p>Se va a producir el siguiente evento durante los días %s.</p><p>%s</p>" % (instance.fecha_simple(), instance.resumen)
            e.excerpt = "Se ha creado un nuevo evento en la agenda"
            e.categories = CategoryZinnia.objects.filter(slug="actividades-externas")
            e.sites = Site.objects.all()
            e.comment_enabled = False
            e.save()
        else:
            print "No sobreescribo entrada existente", e, e.pk
