from django_filters import BooleanFilter, FilterSet, NumberFilter


class InstrumentFilter(FilterSet):
    dept = NumberFilter(field_name='owner')


class MaterialFilter(FilterSet):
    dept = NumberFilter(field_name='amount', lookup_expr='storage__owner')


class StorageFilter(FilterSet):
    storage = NumberFilter(field_name='parent_storage')
    is_root = BooleanFilter(field_name='parent_storage', lookup_expr='isnull')
