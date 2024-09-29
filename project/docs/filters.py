from django_filters import FilterSet, NumberFilter

from docs.models import Protocol, ProtocolE2


class ProtocolE2Filter(FilterSet):
    year = NumberFilter(field_name='date', lookup_expr='year')

    class Meta:
        model = ProtocolE2
        fields = ['connection']


class ProtocolFilter(FilterSet):
    year = NumberFilter(field_name='date', lookup_expr='year')

    class Meta:
        model = Protocol
        fields = ['connection', 'template']
