from django import template
from django.urls import reverse_lazy

from docs.forms import FloatForm
from docs.models import Float


register = template.Library()


@register.inclusion_tag('docs/base_element.html')
def float_element(slug, protocol_pk, user):
    object = Float.objects.filter(slug=slug, protocol=protocol_pk).first()

    if object:
        return {
            'object': object,
            'url': reverse_lazy('docs:float-update', kwargs={'pk': object.pk}),
            'user': user,
        }

    return {
        'form': FloatForm(),
        'slug': slug,
        'protocol_pk': protocol_pk,
        'url': reverse_lazy('docs:float-create'),
        'user': user,
    }
