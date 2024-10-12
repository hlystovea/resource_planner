from django import template
from django.urls import reverse_lazy

from docs.forms import TextForm
from docs.models import Text


register = template.Library()


@register.inclusion_tag('docs/includes/text_element.html')
def text_element(slug, protocol_pk, user):
    object = Text.objects.filter(protocol=protocol_pk, slug=slug).first()

    if not user.is_authenticated:
        return {'object': object}

    form = TextForm(instance=object)
    url = reverse_lazy('docs:text-create')

    if object:
        url = reverse_lazy('docs:text-update', kwargs={'pk': object.pk})

    return {
        'form': form,
        'slug': slug,
        'protocol_pk': protocol_pk,
        'url': url,
    }
