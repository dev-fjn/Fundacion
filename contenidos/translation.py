# -*- coding: utf-8 -*-

from modeltranslation.translator import translator, TranslationOptions
from contenidos.models import Imagen, Video

class MediaTranslationOptions(TranslationOptions):
    '''Traducción.'''

    fields = ('titulo', )

translator.register(Imagen, MediaTranslationOptions)
translator.register(Video, MediaTranslationOptions)



