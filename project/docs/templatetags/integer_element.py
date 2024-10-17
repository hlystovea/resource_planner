from django import template
from django.urls import reverse_lazy

from docs.forms import IntegerForm
from docs.models import Integer


register = template.Library()


@register.inclusion_tag('docs/base_element.html')
def integer_element(slug, protocol_pk, user):
    object = Integer.objects.filter(slug=slug, protocol=protocol_pk).first()

    if object:
        url = reverse_lazy('docs:integer-update', kwargs={'pk': object.pk})
        return {
            'object': object,
            'url': url,
            'user': user,
        }

    return {
        'form': IntegerForm(),
        'slug': slug,
        'protocol_pk': protocol_pk,
        'url': reverse_lazy('docs:integer-create'),
        'user': user,
    }
