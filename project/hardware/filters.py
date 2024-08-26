from django_filters import FilterSet, NumberFilter, CharFilter

from hardware.models import Cabinet, Component, Connection, Hardware, Part


class ComponentFilter(FilterSet):
    dept = NumberFilter(field_name='amount', lookup_expr='storage__owner')
    search = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Component
        fields = ['amount', 'manufacturer']


class ConnectionFilter(FilterSet):
    class Meta:
        model = Connection
        fields = ['facility']


class HardwareFilter(FilterSet):
    facility = NumberFilter(field_name='connection', lookup_expr='facility')

    class Meta:
        model = Hardware
        fields = ['connection', 'group']


class CabinetFilter(FilterSet):
    class Meta:
        model = Cabinet
        fields = ['hardware']


class PartFilter(FilterSet):
    class Meta:
        model = Part
        fields = ['cabinet']
