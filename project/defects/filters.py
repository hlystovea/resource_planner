from django_filters import FilterSet, NumberFilter, BooleanFilter

from defects.models import Defect


class DefectFilter(FilterSet):
    year = NumberFilter(field_name='date', lookup_expr='year')
    unrepaired = BooleanFilter(field_name='repair_date', lookup_expr='isnull')

    facility = NumberFilter(field_name='part', lookup_expr='cabinet__hardware__connection__facility')  # noqa(E501)
    connection = NumberFilter(field_name='part', lookup_expr='cabinet__hardware__connection')  # noqa(E501)
    group = NumberFilter(field_name='part', lookup_expr='cabinet__hardware__group')
    hardware = NumberFilter(field_name='part', lookup_expr='cabinet__hardware')
    cabinet = NumberFilter(field_name='part', lookup_expr='cabinet')

    class Meta:
        model = Defect
        fields = ['part', 'employee']
