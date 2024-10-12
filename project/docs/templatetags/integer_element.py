from django import template
from django.urls import reverse_lazy

from docs.forms import IntegerForm
from docs.models import Integer


register = template.Library()


@register.inclusion_tag('docs/includes/base_element.html')
def integer_element(slug, protocol_pk, user):
    object = Integer.objects.filter(slug=slug, protocol=protocol_pk).first()

    if object:
        return {
            'object': object,
        }

    return {
        'form': IntegerForm(),
        'slug': slug,
        'protocol_pk': protocol_pk,
        'user': user,
        'url': reverse_lazy('docs:integer-create'),
    }
