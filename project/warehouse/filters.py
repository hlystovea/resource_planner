from django_filters import FilterSet, NumberFilter

from warehouse.models import Instrument, Material


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
