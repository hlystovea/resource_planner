from django import template
from django.urls import reverse_lazy

from docs.forms import FloatForm
from docs.models import Float


register = template.Library()


@register.inclusion_tag('docs/includes/float_element.html')
def float_element(slug, protocol_pk, user):
    object = Float.objects.filter(slug=slug, protocol=protocol_pk).first()

    if not user.is_authenticated:
        return {'object': object}

    form = FloatForm(instance=object)
    url = reverse_lazy('docs:float-create')

    if object:
        url = reverse_lazy('docs:float-update', kwargs={'pk': object.pk})

    return {
        'form': form,
        'slug': slug,
        'protocol_pk': protocol_pk,
        'url': url,
    }
