from django import template

from docs.forms import ImageForm
from docs.models import File


register = template.Library()


@register.inclusion_tag('docs/includes/image_element.html')
def image_element(slug, protocol_pk):
    obj = File.objects.filter(protocol=protocol_pk, slug=slug)

    if obj.exists():
        return {'image': obj.first()}

    return {'form': ImageForm(), 'slug': slug, 'protocol_pk': protocol_pk}
