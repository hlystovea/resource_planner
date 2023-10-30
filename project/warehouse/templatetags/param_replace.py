from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Based on
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    query_params = context['request'].GET.copy()

    for key, value in kwargs.items():
        query_params[key] = value

    for key in [key for key, value in query_params.items() if not value]:
        del query_params[key]

    return query_params.urlencode()
