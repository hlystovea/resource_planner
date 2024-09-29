from django import template

from docs.forms import TextForm
from docs.models import Text


register = template.Library()


@register.inclusion_tag('docs/includes/text_element.html')
def text_element(slug, protocol_pk):
    obj = Text.objects.filter(protocol=protocol_pk, slug=slug)

    if obj.exists():
        return {'text': obj.first()}

    return {'form': TextForm(), 'slug': slug, 'protocol_pk': protocol_pk}
