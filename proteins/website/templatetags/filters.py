from django import template

register = template.Library()

@register.filter
def firstLetter(text):
    return text[0].upper()