from django import template
from django.urls import reverse_lazy

from docs.forms import CharForm
from docs.models import Text


register = template.Library()


@register.inclusion_tag('docs/base_element.html')
def char_element(slug, protocol_pk, user):
    object = Text.objects.filter(protocol=protocol_pk, slug=slug).first()

    if object:
        return {
            'object': object,
            'url': reverse_lazy('docs:char-update', kwargs={'pk': object.pk}),
            'user': user,
        }

    return {
        'form': CharForm(),
        'slug': slug,
        'protocol_pk': protocol_pk,
        'url': reverse_lazy('docs:char-create'),
        'user': user,
    }
