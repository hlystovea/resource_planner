from django import template

register = template.Library()


@register.filter
def replace(field, substr, new_substr):
    existing_classes = field.field.widget.attrs.get('class', '').split()
    existing_classes = set(existing_classes or [])
    existing_classes.add(css)
    return field.as_widget(
        attrs={'class': ' '.join(existing_classes)}
    )
