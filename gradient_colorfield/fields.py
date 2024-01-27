#!/usr/bin/env python

import re

from django import forms
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

color_re = re.compile('^to\s?(\bbottom|\bright|\btop left|\btop right|\btop)\s#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
validate_color = RegexValidator(color_re, _('Enter a valid gradient color.'), 'invalid')


class GradientColorField(models.CharField):
    # default_validators = [validate_color]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 100
        super(GradientColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = GradientColorWidget
        return super(GradientColorField, self).formfield(**kwargs)


class GradientColorWidget(forms.Widget):
    class Media:
        js = ('gradient_colorfield/lgcolor/lgcolor.js',)
        css = {
            'all': ('gradient_colorfield/lgcolor/lgcolor.css',)
        }

    def render(self, name, value, attrs=None, renderer=None, **_kwargs):
        is_required = self.is_required
        return render_to_string('gradient_colorfield/gradient_color.html', locals())

    def value_from_datadict(self, data, files, name):
        ret = super(GradientColorWidget, self).value_from_datadict(data, files, name)
        ret = '{}'.format(ret) if ret else ret
        return ret


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^gradient_colorfield\.fields\.GradientColorField"])
except ImportError:
    pass



