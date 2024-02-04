from django import template

register = template.Library()


@register.filter
def is_root(storage):
    return storage.filter(parent_storage__isnull=True)
