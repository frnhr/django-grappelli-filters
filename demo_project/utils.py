# coding=utf-8
from __future__ import unicode_literals
from django.utils.safestring import mark_safe


def str_list_of_objects(iretable_):
    return mark_safe('<br />\n'.join(map(str, iretable_)))
