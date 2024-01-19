from django_filters import FilterSet, NumberFilter

from warehouse.models import Instrument, Material, Storage


class InstrumentFilter(FilterSet):
    dept = NumberFilter(field_name='owner')

    class Meta:
        model = Instrument
        fields = ['owner']


class MaterialFilter(FilterSet):
    dept = NumberFilter(field_name='amount', lookup_expr='owner')

    class Meta:
        model = Material
        fields = ['amount']


class StorageFilter(FilterSet):
    storage = NumberFilter(field_name='parent_storage')

    class Meta:
        model = Storage
        fields = ['parent_storage']
