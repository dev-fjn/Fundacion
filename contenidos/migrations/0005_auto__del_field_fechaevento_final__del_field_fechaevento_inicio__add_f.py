# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'FechaEvento.final'
        db.delete_column(u'contenidos_fechaevento', 'final')

        # Deleting field 'FechaEvento.inicio'
        db.delete_column(u'contenidos_fechaevento', 'inicio')

        # Adding field 'FechaEvento.fecha'
        db.add_column(u'contenidos_fechaevento', 'fecha',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 10, 28, 0, 0)),
                      keep_default=False)

        # Adding field 'FechaEvento.hora_inicio'
        db.add_column(u'contenidos_fechaevento', 'hora_inicio',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2013, 10, 28, 0, 0)),
                      keep_default=False)

        # Adding field 'FechaEvento.hora_final'
        db.add_column(u'contenidos_fechaevento', 'hora_final',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2013, 10, 28, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'FechaEvento.final'
        raise RuntimeError("Cannot reverse this migration. 'FechaEvento.final' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'FechaEvento.inicio'
        raise RuntimeError("Cannot reverse this migration. 'FechaEvento.inicio' and its values cannot be restored.")
        # Deleting field 'FechaEvento.fecha'
        db.delete_column(u'contenidos_fechaevento', 'fecha')

        # Deleting field 'FechaEvento.hora_inicio'
        db.delete_column(u'contenidos_fechaevento', 'hora_inicio')

        # Deleting field 'FechaEvento.hora_final'
        db.delete_column(u'contenidos_fechaevento', 'hora_final')


    models = {
        u'contenidos.evento': {
            'Meta': {'object_name': 'Evento'},
            'fecha_y_lugar': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'resumen': ('django.db.models.fields.TextField', [], {}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'contenidos.fechaevento': {
            'Meta': {'object_name': 'FechaEvento'},
            'evento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenidos.Evento']"}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'hora_final': ('django.db.models.fields.TimeField', [], {}),
            'hora_inicio': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'contenidos.imagen': {
            'Meta': {'ordering': "('orden',)", 'object_name': 'Imagen'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'orden': ('django.db.models.fields.IntegerField', [], {'default': '20'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'titulo_en': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'titulo_es': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'contenidos.lugarevento': {
            'Meta': {'object_name': 'LugarEvento'},
            'evento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenidos.Evento']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitud': ('django.db.models.fields.FloatField', [], {}),
            'longitud': ('django.db.models.fields.FloatField', [], {})
        },
        u'contenidos.video': {
            'Meta': {'object_name': 'Video'},
            'flv_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mp4_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'titulo_en': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'titulo_es': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['contenidos']