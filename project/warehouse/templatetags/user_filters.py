from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})
