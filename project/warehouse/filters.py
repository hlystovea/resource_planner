from django.db.models import Q
from django_filters import BooleanFilter, CharFilter, FilterSet, NumberFilter


class InstrumentFilter(FilterSet):
    dept = NumberFilter(field_name='owner')
    search = CharFilter(method='search_filter')

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            | Q(inventory_number__icontains=value)
            | Q(serial_number__icontains=value)
        )


class MaterialFilter(FilterSet):
    dept = NumberFilter(field_name='amount', lookup_expr='storage__owner')
    search = CharFilter(method='search_filter')

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(article_number__icontains=value)
        )
