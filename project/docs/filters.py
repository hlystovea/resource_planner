from django_filters import FilterSet, NumberFilter

from docs.models import Protocol


class ProtocolFilter(FilterSet):
    year = NumberFilter(field_name='date', lookup_expr='year')
    connection = NumberFilter(field_name='hardware', lookup_expr='connection')

    class Meta:
        model = Protocol
        fields = ['hardware', 'template']
