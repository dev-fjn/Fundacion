# -*- coding: utf-8 -*-

'''Administración del módulo.

'''

from django.contrib import admin
from blog.models import *


class PostAdmin(admin.ModelAdmin):
    ''' PostAdmin '''

    search_fields = ['title']
    display_fields = 'title created'.split()


class CommentAdmin(admin.ModelAdmin):
    ''' CommentAdmin '''

    display_fields = 'post author created'.split()


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
