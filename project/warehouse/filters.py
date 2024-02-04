from django_filters import BooleanFilter, CharFilter, FilterSet, NumberFilter


class InstrumentFilter(FilterSet):
    dept = NumberFilter(field_name='owner')
    search = CharFilter(field_name='name', lookup_expr='icontains')


class MaterialFilter(FilterSet):
    dept = NumberFilter(field_name='amount', lookup_expr='storage__owner')
    search = CharFilter(field_name='name', lookup_expr='icontains')


class StorageFilter(FilterSet):
    storage = NumberFilter(field_name='parent_storage')
    is_root = BooleanFilter(field_name='parent_storage', lookup_expr='isnull')
