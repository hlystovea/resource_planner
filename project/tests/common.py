def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


def get_field_context(context, field_type):
    for fld in context.keys():
        if fld not in ('user', 'request') and type(context[fld]) == field_type:
            return context[fld]
