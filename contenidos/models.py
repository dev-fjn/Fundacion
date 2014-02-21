# -*- coding: utf-8 -*-

from django.contrib.sites.models import Site
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from filebrowser.fields import FileBrowseField
from zinnia.models import Category as CategoryZinnia, Entry as EntryZinnia
import datetime
import os

#
# FUNCIONES/CLASES AUXILIARES
# 

def _siguiente_orden():
    m = Carrusel.objects.aggregate(models.Max("orden"))["orden__max"]
    return 1 if not m else m+1

EXTENSIONES_IMAGEN = ['.png', '.jpg', '.jpeg', '.gif', '.svg']
EXTENSIONES_AUDIO = ['.mp3', '.ogg', '.wav']
EXTENSIONES_VIDEO = ['.flv', '.mp4', '.ogv', '.webm']

COLETILLAS_AUDIO = [
    ('.mp3', 'audio/mpeg'),
    ('.ogg', 'audio/ogg'),
]

COLETILLAS_VIDEO = [
    ('_libtheora.ogv', 'audio/ogg'),
    ('_VP8.webm', 'audio/webm'),
    ('_x264.mp4', 'audio/mp4'),
    ('.ogv', 'audio/ogg'),
    ('.webm', 'audio/webm'),
    ('.mp4', 'audio/mp4'),
]

class ComunesMultimedia(object):
    # Esta clase asume que existe "self.filename" que es un FileBrowseField, 
    # pero, aunque podria, no pongo ese field aqui ya que cada hijo lo lleva
    # configurado en una carpeta diferente.

    def extension(self):
        return os.path.splitext(self.filename.path)[1]

    def es_imagen(self):
        return self.extension() in EXTENSIONES_IMAGEN

    def es_audio(self):
        return self.extension() in EXTENSIONES_AUDIO

    def es_video(self):
        return self.extension() in EXTENSIONES_VIDEO

    def _busca_por_coletillas(self, lista_coletillas):
        fichero_sin_coletilla = None
        for coletilla, extension in lista_coletillas:
            if self.filename.path.endswith(coletilla):
                fichero_sin_coletilla = self.filename.path[:-len(coletilla)]
                break
        else:
            # Si la extension no coincide con ninguna de la coletilla... no hacemos nada
            return
        # mostramos todos los ficheros/extension que coincidan y esten en el sistema de archivos
        for coletilla, extension in lista_coletillas:
            fichero = fichero_sin_coletilla + coletilla
            if os.path.isfile(os.path.join(settings.MEDIA_ROOT, fichero)):
                yield fichero, extension

    def busca_videos_extensiones(self):
        return self._busca_por_coletillas(COLETILLAS_VIDEO)

    def busca_audios_extensiones(self):
        return self._busca_por_coletillas(COLETILLAS_AUDIO)

#
# MODELOS DE DJANGO
# 

class Carrusel(ComunesMultimedia, models.Model):
    titulo = models.CharField(max_length=250)
    orden = models.IntegerField(default=_siguiente_orden)
    filename = FileBrowseField("fichero", max_length=200, directory="carrusel")

    class Meta:
        verbose_name = u'carrusel'
        verbose_name_plural = u'carruseles'
        ordering = ('orden', )


class Evento(models.Model):
    titulo = models.CharField(max_length=250)
    resumen = models.TextField()
    fecha_y_lugar = models.TextField()
    imagen = models.ImageField(upload_to="eventos/imagenes", blank=True, null=True)
    pdf = models.FileField(upload_to="eventos/pdf", blank=True, null=True)

    def __unicode__(self):
        return u"%s" % (self.titulo, )
    
    class Meta:
        # CUIDADO CUIDADO: Si aparecen efectos de duplicidad de eventos, hay que quitar esto.
        # De momento solo lo veo en /admin/contenidos/evento/ con lo cual está limitado.
        # Pero es que si no me aparecen desordenados y es feo.
        ordering = ('fechaevento__fecha_inicio', )

    def fecha_simple(self):
        return ", ".join([ev.simple() for ev in self.fechaevento_set.all()])

    @staticmethod
    def datos_para_calendario(start, end):
        qs = FechaEvento.objects.filter(fecha_inicio__gte=start, fecha_final__lte=end)
        # clasificamos los resultados por dias
        v = {}
        for fe in qs:
            dias = (fe.fecha_final-fe.fecha_inicio).days
            if dias >= settings.MAXIMOS_DIAS_SEGUIDOS_CALENDARIO:
                continue # pasamos de pintar cuando hay eventos de más de una semana porque nos va a colorear todo el calendario
            elif dias < 0:
                continue # no mola ir hacia atras en el bucle siguiente
            dmy = fe.fecha_inicio
            while True:
                if not dmy in v:
                    v[dmy] = []
                v[dmy].append(fe.evento)
                if dmy == fe.fecha_final:
                    break
                else:
                    dmy += datetime.timedelta(days=1)
        return v
    

class FechaEvento(models.Model):
    evento = models.ForeignKey(Evento)
    fecha_inicio = models.DateField(help_text=u"Fecha de inicio del evento")
    fecha_final = models.DateField(blank=True, null=True, help_text=u"Fecha final del evento inclusive (de no escribir nada se pondrá igual a la fecha de inicio)")
    hora_inicio = models.TimeField(blank=True, null=True, help_text=u"Hora inicio del evento, vacío si todo el dia")
    hora_final = models.TimeField(blank=True, null=True, help_text=u"Hora final del evento (de no escribir nada se pondrá igual que la hora de inicio)")

    def fechas(self):
        if self.fecha_final and self.fecha_inicio != self.fecha_final:
            return u"%s...%s" % (self.fecha_inicio, self.fecha_final)
        else:
            return u"%s" % (self.fecha_inicio, )

    def horas(self):
        if self.hora_inicio and self.hora_final:
            return u"%s...%s" % (self.hora_inicio, self.hora_final)
        else:
            return u"todo el día"

    def simple(self):
        return u"%s (%s)" % (self.fechas(), self.horas())

    def __unicode__(self):
        return u"%s %s (%s)" % (self.fechas(), self.horas(), self.evento)

    class Meta:
        ordering = ('fecha_inicio', )


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
    tipo = models.CharField(max_length=40, choices=TIPO.CHOICES, default=TIPO.LIBRO, blank=True, null=True)
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

    def get_absolute_url(self):
        if self.precio:
            return reverse('publicacion_detalle', args=[str(self.id)])
        else:
            return reverse('libro_detalle', args=[str(self.id)])

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

class Categoria(models.Model):
    tipo = models.IntegerField(choices=TIPO.CHOICES)
    nombre = models.CharField(max_length=250, help_text=u"El nombre de la categoria, si hay más de uno", blank=True, null=True)

    class Meta:
        ordering = ('tipo', 'nombre')
        unique_together = ( ('tipo', 'nombre'), )
        verbose_name = u'Categoría de documentos'
        verbose_name_plural = u'Categorías de documentos'

    def __unicode__(self):
        if self.nombre:
            return u"%s - %s" % (self.get_tipo_display(), self.nombre)
        else:
            return u"%s" % (self.get_tipo_display(), )

class Autor(models.Model):
    nombre = models.CharField(max_length=250)

    def __unicode__(self):
        return self.nombre

    class Meta:
        ordering = ('nombre', )
        verbose_name = u'Autor'
        verbose_name_plural = u'Autores'

class Documento(models.Model):
    categoria = models.ForeignKey(Categoria)
    titulo = models.CharField(max_length=250, help_text=u"El título principal del documento")
    slug = models.SlugField(help_text=u"La url que aparecerá en el navegador cuando se visualice el detalle de este documento (autogenerado)")
    autor = models.ForeignKey(Autor, blank=True, null=True)
    descripcion = models.TextField(help_text=u"Escribir un resumen del documento, si es una entrevista detallar el entrevistado", blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    fuente = models.CharField(max_length=250, help_text=u"La fuente del documento, si procede, o el nombre del periódico", blank=True, null=True)

    def adjuntos(self):
        l = list(self.urladjunto_set.all())
        l += list(self.ficheroadjunto_set.all())
        return sorted(l, key=lambda x: x.titulo)
    
    def get_absolute_url(self):
        if self.categoria.tipo == TIPO.RECURSOS_AUDIOVISUALES:
            return reverse('recurso_audiovisual_detalle', args=[self.slug])
        elif self.categoria.tipo == TIPO.PRESENCIA_EN_PRENSA:
            return reverse('presencia_en_prensa_detalle', args=[self.slug])
        elif self.categoria.tipo == TIPO.DOSSIERES_DE_PRENSA:
            return reverse('dossier_de_prensa_detalle', args=[self.slug])
        else:
            raise RuntimeError("Tipo no soportado")

    def __unicode__(self):
        return u"%s: %s" % (self.categoria, self.titulo)

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
    miniatura = FileBrowseField("miniaturas", max_length=200, directory="documentos/miniaturas", help_text=u"Miniatura del contenido, si procede", blank=True, null=True)

    class Meta:
        verbose_name = u'Referencia al documento en internet'
        verbose_name_plural = u'Referencias al documento en internet'

class FicheroAdjunto(ComunesMultimedia, Adjunto):
    # NO-FIXME no hay mucha forma de que segun el tipo de contenido cambie la carpeta, y como tendremos media (videos) y documentos, hay que disparar al raiz
    #filename = FileBrowseField("fichero", max_length=200, directory="documentos")
    #miniatura = FileBrowseField("miniaturas", max_length=200, directory="documentos/miniaturas", help_text=u"Miniatura del contenido, si procede", blank=True, null=True)
    filename = FileBrowseField("fichero", max_length=200, directory="")
    miniatura = FileBrowseField("miniaturas", max_length=200, directory="", help_text=u"Miniatura del contenido, si procede", blank=True, null=True)

    class Meta:
        verbose_name = u'Enlace al documento almacenado por FTP'
        verbose_name_plural = u'Enlaces al documento almacenado por FTP'

class CitaDe(models.Model):
    contenido = models.TextField(help_text=u"Poner el texto que se cita")
    descripcion = models.CharField('descripción', max_length=250, help_text="Evento (y lugar) donde se realizó", default=u"Discurso")
    fecha = models.DateField(help_text="Escribir fecha exacta (o fecha de ordenación)")
    fecha_literal = models.CharField(max_length=250, blank=True, null=True, help_text="Escribir fecha a mostrar (en blanco si es exacta, escribir algo si es ambigua o no se conoce la exacta)")

    def __unicode__(self):
        return u"%s" % (self.contenido, )

    class Meta:
        ordering = ('fecha', )
        verbose_name = u'cita de Juan Negrín'
        verbose_name_plural = u'citas de Juan Negrín'

class CitaSobre(models.Model):
    contenido = models.TextField(help_text=u"Poner el texto que se cita")
    autor = models.CharField(max_length=250, help_text="Autor de la cita")
    cargo = models.CharField(max_length=250, blank=True, null=True, help_text="Cargo del autor (si procede)")
    fecha = models.DateField(blank=True, null=True, help_text="Escribir fecha exacta (o fecha de ordenación)")
    fecha_literal = models.CharField(max_length=250, blank=True, null=True, help_text="Escribir fecha a mostrar (en blanco si es exacta, escribir algo si es ambigua o no se conoce la exacta)")

    def __unicode__(self):
        return u"%s: %s" % (self.contenido, self.autor)

    class Meta:
        ordering = ('autor', )
        verbose_name = u'cita sobre Juan Negrín'
        verbose_name_plural = u'citas sobre Juan Negrín'

class Presencia(models.Model):
    denominacion = models.CharField(max_length=250)
    lugar = models.CharField(max_length=250)
    url_lugar = models.URLField(blank=True, null=True)
    descripcion = models.TextField()
    imagen = FileBrowseField("Imagen", max_length=200, directory="presencia")
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.denominacion, self.lugar)

#
# SEÑALES
# 

@receiver(pre_save, sender=FechaEvento)
def asigna_finales_al_guardar(sender, instance, **kwargs):
    # no pueden ser vacias
    if not instance.fecha_final:
        instance.fecha_final = instance.fecha_inicio
    if not instance.hora_final:
        instance.hora_final = instance.hora_inicio
    # no pueden estar al reves, les damos la vuelta
    if instance.fecha_final < instance.fecha_inicio:
        instance.fecha_final, instance.fecha_inicio = instance.fecha_inicio, instance.fecha_final
    if instance.hora_final < instance.hora_inicio:
        instance.hora_final, instance.hora_inicio = instance.hora_inicio, instance.hora_final

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
