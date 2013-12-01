# -*- coding: utf-8 -*-

from modeltranslation.translator import translator, TranslationOptions
from contenidos.models import Carrusel

class MediaTranslationOptions(TranslationOptions):
    '''Traducción.'''

    fields = ('titulo', )

translator.register(Carrusel, MediaTranslationOptions)



