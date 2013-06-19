# -*- coding: utf-8 -*-

'''Formularios para el blog.

'''

from django.forms import *
from blog.models import *


class CommentForm(ModelForm):
    ''' CommentForm '''


    class Meta:
        ''' Meta '''

        model = Comment
        exclude = ['post']


    def clean_author(self):
        '''clean_author'''

        return self.cleaned_data.get('author') or 'Anonymous'

