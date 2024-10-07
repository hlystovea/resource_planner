from django_filters import FilterSet, NumberFilter

from docs.models import Protocol


class ProtocolFilter(FilterSet):
    year = NumberFilter(field_name='date', lookup_expr='year')

    class Meta:
        model = Protocol
        fields = ['connection', 'template']
