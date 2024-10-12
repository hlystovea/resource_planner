from django import template
from django.urls import reverse_lazy

from docs.forms import CharForm
from docs.models import Text


register = template.Library()


@register.inclusion_tag('docs/includes/char_element.html')
def char_element(slug, protocol_pk, user):
    object = Text.objects.filter(protocol=protocol_pk, slug=slug).first()

    if not user.is_authenticated:
        return {'object': object}

    form = CharForm(instance=object)
    url = reverse_lazy('docs:char-create')

    if object:
        url = reverse_lazy('docs:char-update', kwargs={'pk': object.pk})

    return {
        'form': form,
        'slug': slug,
        'protocol_pk': protocol_pk,
        'url': url,
    }
