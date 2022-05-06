from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def split(value):
    
    return value.split(", ")

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
@stringfilter
def newline(value):
    return value.split("\n")

@register.filter(name='zip')
def zip_lists(a, b):
  return zip(a, b)
