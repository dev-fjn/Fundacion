# -*- coding: utf-8 -*-

from django import template
register = template.Library()

from django.conf import settings
from flatpages_i18n.models import FlatPage_i18n

@register.inclusion_tag('contenidos/_flatblock.html', takes_context=True)
def flatblock(context, flatpage_url):
    try:
        obj = FlatPage_i18n.objects.get(url=flatpage_url)
    except FlatPage_i18n.DoesNotExist:
        return {}
    return {
        'user': context.get('user'),
        'object': obj,
        'flatpage_url': flatpage_url,
    }

