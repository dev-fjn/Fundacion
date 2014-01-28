# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FechaEvento.fecha_final'
        db.add_column(u'contenidos_fechaevento', 'fecha_final',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'FechaEvento.hora_final'
        db.alter_column(u'contenidos_fechaevento', 'hora_final', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'FechaEvento.hora_inicio'
        db.alter_column(u'contenidos_fechaevento', 'hora_inicio', self.gf('django.db.models.fields.TimeField')(null=True))

    def backwards(self, orm):
        # Deleting field 'FechaEvento.fecha_final'
        db.delete_column(u'contenidos_fechaevento', 'fecha_final')


        # User chose to not deal with backwards NULL issues for 'FechaEvento.hora_final'
        raise RuntimeError("Cannot reverse this migration. 'FechaEvento.hora_final' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'FechaEvento.hora_final'
        db.alter_column(u'contenidos_fechaevento', 'hora_final', self.gf('django.db.models.fields.TimeField')())

        # User chose to not deal with backwards NULL issues for 'FechaEvento.hora_inicio'
        raise RuntimeError("Cannot reverse this migration. 'FechaEvento.hora_inicio' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'FechaEvento.hora_inicio'
        db.alter_column(u'contenidos_fechaevento', 'hora_inicio', self.gf('django.db.models.fields.TimeField')())

    models = {
        u'contenidos.autor': {
            'Meta': {'ordering': "('nombre',)", 'object_name': 'Autor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'contenidos.carrusel': {
            'Meta': {'ordering': "('orden',)", 'object_name': 'Carrusel'},
            'filename': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orden': ('django.db.models.fields.IntegerField', [], {'default': '28'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'titulo_en': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'titulo_es': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'contenidos.categoria': {
            'Meta': {'ordering': "('tipo', 'nombre')", 'unique_together': "(('tipo', 'nombre'),)", 'object_name': 'Categoria'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.IntegerField', [], {})
        },
        u'contenidos.citade': {
            'Meta': {'ordering': "('fecha',)", 'object_name': 'CitaDe'},
            'contenido': ('django.db.models.fields.TextField', [], {}),
            'descripcion': ('django.db.models.fields.CharField', [], {'default': "u'Discurso'", 'max_length': '250'}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'fecha_literal': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'contenidos.citasobre': {
            'Meta': {'ordering': "('autor',)", 'object_name': 'CitaSobre'},
            'autor': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'cargo': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'contenido': ('django.db.models.fields.TextField', [], {}),
            'fecha': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_literal': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'contenidos.documento': {
            'Meta': {'object_name': 'Documento'},
            'autor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenidos.Autor']", 'null': 'True', 'blank': 'True'}),
            'categoria': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenidos.Categoria']"}),
            'descripcion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fuente': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'contenidos.evento': {
            'Meta': {'ordering': "('fechaevento__fecha',)", 'object_name': 'Evento'},
            'fecha_y_lugar': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'resumen': ('django.db.models.fields.TextField', [], {}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'contenidos.fechaevento': {
            'Meta': {'ordering': "('fecha_inicio',)", 'object_name': 'FechaEvento'},
            'evento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenidos.Evento']"}),
            'fecha_final': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_inicio': ('django.db.models.fields.DateField', [], {}),
            'hora_final': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'hora_inicio': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'contenidos.ficheroadjunto': {
            'Meta': {'object_name': 'FicheroAdjunto'},
            'documento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenidos.Documento']"}),
            'filename': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'miniatura': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'contenidos.libro': {
            'Meta': {'object_name': 'Libro'},
            'autor': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'editorial': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idioma': ('django.db.models.fields.CharField', [], {'default': "u'Castellano'", 'max_length': '40'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '17', 'null': 'True', 'blank': 'True'}),
            'miniatura': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'pais': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'precio': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'resumen': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': "u'Libro'", 'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'contenidos.presencia': {
            'Meta': {'object_name': 'Presencia'},
            'denominacion': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            'latitud': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitud': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lugar': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'url_lugar': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'contenidos.urladjunto': {
            'Meta': {'object_name': 'UrlAdjunto'},
            'documento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenidos.Documento']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'miniatura': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['contenidos']