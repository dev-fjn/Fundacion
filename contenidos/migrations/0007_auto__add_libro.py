# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Libro'
        db.create_table(u'contenidos_libro', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('autor', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('fecha', self.gf('django.db.models.fields.DateField')()),
            ('precio', self.gf('django.db.models.fields.FloatField')()),
            ('miniatura', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('resumen', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'contenidos', ['Libro'])


    def backwards(self, orm):
        # Deleting model 'Libro'
        db.delete_table(u'contenidos_libro')


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
        u'contenidos.libro': {
            'Meta': {'object_name': 'Libro'},
            'autor': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'miniatura': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'precio': ('django.db.models.fields.FloatField', [], {}),
            'resumen': ('django.db.models.fields.TextField', [], {}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
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