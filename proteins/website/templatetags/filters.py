

from django import template

register = template.Library()

@register.filter
def pairs(list_obj):
    return [(list_obj[i],list_obj[i+1]) for i in range(0,len(list_obj)-1,2)]

    