import django_filters

from warehouse.models import Material


class MaterialFilter(django_filters.FilterSet):
    class Meta:
        model = Material
        fields = ['amount__storage']
