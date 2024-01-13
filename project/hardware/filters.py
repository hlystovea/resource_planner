from django_filters import FilterSet, NumberFilter

from hardware.models import Cabinet, Component, Connection, Hardware, Part


class ComponentFilter(FilterSet):
    owner = NumberFilter(field_name='amount', lookup_expr='owner')

    class Meta:
        model = Component
        fields = ['amount', 'manufacturer']


class ConnectionFilter(FilterSet):
    class Meta:
        model = Connection
        fields = ['facility']


class HardwareFilter(FilterSet):
    class Meta:
        model = Hardware
        fields = ['connection']


class CabinetFilter(FilterSet):
    class Meta:
        model = Cabinet
        fields = ['hardware']


class PartFilter(FilterSet):
    class Meta:
        model = Part
        fields = ['cabinet']
