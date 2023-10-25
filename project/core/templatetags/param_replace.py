from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Based on
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    query_params = context['request'].GET.copy()
    query_params = query_params | kwargs
    query_params = {key: value for key, value in query_params.items() if value}
    return query_params.urlencode()
