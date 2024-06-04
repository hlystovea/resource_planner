from django_filters import FilterSet, NumberFilter

from docs.models import ProtocolE2


class ProtocolE2Filter(FilterSet):
    year = NumberFilter(field_name='date', lookup_expr='year')

    class Meta:
        model = ProtocolE2
        fields = ['connection']
