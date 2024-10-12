from django import template
from django.urls import reverse_lazy

from docs.forms import IntegerForm
from docs.models import Integer


register = template.Library()


@register.inclusion_tag('docs/includes/integer_element.html')
def integer_element(slug, protocol_pk, user):
    object = Integer.objects.filter(slug=slug, protocol=protocol_pk).first()

    if not user.is_authenticated:
        return {'object': object}

    form = IntegerForm(instance=object)
    url = reverse_lazy('docs:integer-create')

    if object:
        url = reverse_lazy('docs:integer-update', kwargs={'pk': object.pk})

    return {
        'form': form,
        'slug': slug,
        'protocol_pk': protocol_pk,
        'url': url,
    }
