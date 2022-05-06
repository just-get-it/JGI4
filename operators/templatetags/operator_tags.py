from django import template

register=template.Library()

@register.filter
def strtolist(string): 
    return list(string.split(","))

@register.filter(name='zip')
def zip_lists(a, b):
  return zip(a, b)

@register.filter()
def to_int(value):
    return int(value)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def mul(val):
    return val*20

@register.filter
def get_achieved(oplist):
    achieve=0
    for a,b in oplist:
    	if a == 'dart_stitch':
    		achieve=achieve+((int(b)*4)/100)
    	elif a=='panel_attach':
    		achieve=achieve+((int(b)*3)/100)
    	elif a=='dart_and_panel_pressing':
    		achieve=achieve+((int(b)*5)/100)
    	elif a=='centre_back_stitch':
    		achieve=achieve+((int(b)*2)/100)
    	elif a=='diamond_stitch':
    		achieve=achieve+((int(b)*3)/100)
    	elif a=='chest_welt_iron':
    		achieve=achieve+((int(b)*1)/100)
    	elif a=='chest_welt_attach':
    		achieve=achieve+((int(b)*4)/100)
    	elif a=='side_seam':
    		achieve=achieve+((int(b)*3)/100)
    return achieve
