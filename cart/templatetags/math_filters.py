from django import template
from django.template import TemplateSyntaxError

register = template.Library()


@register.filter
def multiply(value, arg):
    return value * arg
