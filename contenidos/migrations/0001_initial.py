# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Imagen'
        db.create_table(u'contenidos_imagen', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activo', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('titulo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('titulo_es', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True, blank=True)),
            ('titulo_en', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True, blank=True)),
            ('orden', self.gf('django.db.models.fields.IntegerField')(default=1, unique=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('imagen', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'contenidos', ['Imagen'])

        # Adding model 'Video'
        db.create_table(u'contenidos_video', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activo', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('titulo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('titulo_es', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True, blank=True)),
            ('titulo_en', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True, blank=True)),
            ('flv_url', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('mp4_url', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'contenidos', ['Video'])


    def backwards(self, orm):
        # Deleting model 'Imagen'
        db.delete_table(u'contenidos_imagen')

        # Deleting model 'Video'
        db.delete_table(u'contenidos_video')


    models = {
        u'contenidos.imagen': {
            'Meta': {'ordering': "('orden',)", 'object_name': 'Imagen'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'orden': ('django.db.models.fields.IntegerField', [], {'default': '1', 'unique': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'titulo_en': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'titulo_es': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'contenidos.video': {
            'Meta': {'object_name': 'Video'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flv_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mp4_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'titulo_en': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'titulo_es': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['contenidos']