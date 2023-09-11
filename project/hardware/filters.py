from django_filters import FilterSet, NumberFilter

from hardware.models import Component


class ComponentFilter(FilterSet):
    owner = NumberFilter(field_name='amount', lookup_expr='owner')

    class Meta:
        model = Component
        fields = ['amount', 'manufacturer']
