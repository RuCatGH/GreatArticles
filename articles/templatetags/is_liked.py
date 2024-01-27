from datetime import datetime

from django import template

from likes.services import is_fan

register = template.Library()


@register.simple_tag(takes_context=True)
def is_liked(context, obj):
    return is_fan(obj, context['user'])

