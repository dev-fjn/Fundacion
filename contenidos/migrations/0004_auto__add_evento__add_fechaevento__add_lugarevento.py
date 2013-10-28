# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Evento'
        db.create_table(u'contenidos_evento', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('resumen', self.gf('django.db.models.fields.TextField')()),
            ('fecha_y_lugar', self.gf('django.db.models.fields.TextField')()),
            ('imagen', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('pdf', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'contenidos', ['Evento'])

        # Adding model 'FechaEvento'
        db.create_table(u'contenidos_fechaevento', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('evento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenidos.Evento'])),
            ('inicio', self.gf('django.db.models.fields.DateTimeField')()),
            ('final', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'contenidos', ['FechaEvento'])

        # Adding model 'LugarEvento'
        db.create_table(u'contenidos_lugarevento', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('evento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenidos.Evento'])),
            ('latitud', self.gf('django.db.models.fields.FloatField')()),
            ('longitud', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'contenidos', ['LugarEvento'])


    def backwards(self, orm):
        # Deleting model 'Evento'
        db.delete_table(u'contenidos_evento')

        # Deleting model 'FechaEvento'
        db.delete_table(u'contenidos_fechaevento')

        # Deleting model 'LugarEvento'
        db.delete_table(u'contenidos_lugarevento')


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
            'final': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateTimeField', [], {})
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