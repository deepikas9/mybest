from django import template
import unicodedata
import re

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None

@register.filter
def slugify(value):
    """
    Converts emoji or string to a slug-safe string.
    E.g. 😍 => u1f60d
    """
    if isinstance(value, str):
        return ''.join(['u{:04x}'.format(ord(char)) for char in value])
    return str(value)
