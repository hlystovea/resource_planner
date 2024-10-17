from django import template
from django.urls import reverse_lazy

from docs.forms import ImageForm
from docs.models import File


register = template.Library()


@register.inclusion_tag('docs/image_element.html')
def image_element(slug, protocol_pk, user):
    object = File.objects.filter(protocol=protocol_pk, slug=slug).first()

    if object:
        return {
            'object': object,
            'url': reverse_lazy('docs:image-delete', kwargs={'pk': object.pk}),
            'user': user,
        }

    return {
        'form': ImageForm(),
        'slug': slug,
        'protocol_pk': protocol_pk,
        'url': reverse_lazy('docs:image-create'),
        'user': user,
    }
