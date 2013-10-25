# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Video', fields ['titulo']
        db.delete_unique(u'contenidos_video', ['titulo'])

        # Removing unique constraint on 'Video', fields ['titulo_es']
        db.delete_unique(u'contenidos_video', ['titulo_es'])

        # Removing unique constraint on 'Video', fields ['titulo_en']
        db.delete_unique(u'contenidos_video', ['titulo_en'])

        # Removing unique constraint on 'Imagen', fields ['titulo']
        db.delete_unique(u'contenidos_imagen', ['titulo'])

        # Removing unique constraint on 'Imagen', fields ['titulo_es']
        db.delete_unique(u'contenidos_imagen', ['titulo_es'])

        # Removing unique constraint on 'Imagen', fields ['titulo_en']
        db.delete_unique(u'contenidos_imagen', ['titulo_en'])

        # Removing unique constraint on 'Imagen', fields ['orden']
        db.delete_unique(u'contenidos_imagen', ['orden'])


    def backwards(self, orm):
        # Adding unique constraint on 'Imagen', fields ['orden']
        db.create_unique(u'contenidos_imagen', ['orden'])

        # Adding unique constraint on 'Imagen', fields ['titulo_en']
        db.create_unique(u'contenidos_imagen', ['titulo_en'])

        # Adding unique constraint on 'Imagen', fields ['titulo_es']
        db.create_unique(u'contenidos_imagen', ['titulo_es'])

        # Adding unique constraint on 'Imagen', fields ['titulo']
        db.create_unique(u'contenidos_imagen', ['titulo'])

        # Adding unique constraint on 'Video', fields ['titulo_en']
        db.create_unique(u'contenidos_video', ['titulo_en'])

        # Adding unique constraint on 'Video', fields ['titulo_es']
        db.create_unique(u'contenidos_video', ['titulo_es'])

        # Adding unique constraint on 'Video', fields ['titulo']
        db.create_unique(u'contenidos_video', ['titulo'])


    models = {
        u'contenidos.imagen': {
            'Meta': {'ordering': "('orden',)", 'object_name': 'Imagen'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'orden': ('django.db.models.fields.IntegerField', [], {'default': '20'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'titulo_en': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'titulo_es': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
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