from django import template

register = template.Library()

@register.filter
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)

@register.filter
def to_and(value):
    return value.replace("&","aanndd")

@register.filter
def subtract(value, arg):
    return value - arg