def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


def get_field_context(context, field_type):
    for field in context.keys():
        if (field not in ('user', 'request')
                and isinstance(context[field], field_type)):
            return context[field]
