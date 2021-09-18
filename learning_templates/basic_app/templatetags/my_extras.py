from django import template

register = template.Library()

# This cuts out all values of 'arg' from string!
@register.filter(name='cut')
def cut(value,arg):
    return value.replace(arg,'')

# register.filter('cut',cut)
