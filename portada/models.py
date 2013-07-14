# -*- coding: utf-8 -*-

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Url(MPTTModel):
    ''' ... '''
    name   = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    url    = models.CharField(max_length=250, unique=True)
    lang   = models.CharField(max_length=10)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return self.name
