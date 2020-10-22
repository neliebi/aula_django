from django import template

register = template.Library()

@register.filter
def pairs(list_obj):
	result = []
	for i in range(0,len(list_obj)-1,2):
		result.append((list_obj[i],list_obj[i+1]))
	return result