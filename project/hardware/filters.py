from django.db.models import Q
from django_filters import FilterSet, NumberFilter, CharFilter

from hardware.models import Cabinet, Component, Connection, Hardware, Part


class ComponentFilter(FilterSet):
    dept = NumberFilter(field_name='amount', lookup_expr='storage__owner')
    search = CharFilter(method='search_filter')

    class Meta:
        model = Component
        fields = ['amount', 'manufacturer']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            | Q(manufacturer__name__icontains=value)
            | Q(type__icontains=value)
        )


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
