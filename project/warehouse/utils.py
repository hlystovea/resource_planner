from django.urls import reverse
from warehouse.models import Storage


def get_tree(objects, parent_pk=None, active_pk=None, parent_field='parent'):
    tree = [obj for obj in objects if obj[parent_field] == parent_pk]

    for obj in tree:
        obj['children'], obj['show'] = get_tree(
            objects, obj['pk'], active_pk, parent_field)
        obj['show'] = obj['show'] or obj['pk'] == active_pk

    return tree, any([obj['show'] for obj in tree])


def get_url(request, storage: Storage) -> str:
    return request.build_absolute_uri(
        reverse('warehouse:storage-detail', kwargs={'pk': storage.pk})
    )
