# coding=utf-8

from django import template

register = template.Library()


@register.filter(name='has_category')
def has_category(event, arg):
    for category in event.categories.all():
        if category.slug == arg:
            return True
