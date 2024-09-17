from django.db.models import Count, F
from django.db.models.functions import ExtractYear
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import (DefectSerializer, StatisticsSerializer,
                             YearSerializer)
from defects.filters import DefectFilter
from defects.models import Defect


class DefectViewSet(ReadOnlyModelViewSet):
    queryset = Defect.objects.all()
    serializer_class = DefectSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DefectFilter

    @action(methods=['get'], url_name='years', detail=False)
    def years(self, request, *args, **kwargs):
        years = Defect.objects.dates(
            'date', 'year'
        ).values_list(
            ExtractYear('date'),
            flat=True
        )
        serializer = YearSerializer(instance={'years': years})
        return Response(serializer.data)

    @action(methods=['get'], url_name='statistics-by-year', detail=False)
    def statistics_by_year(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).annotate(
            year=ExtractYear('date')
        ).values(
            label=F('year')
        ).annotate(
            value=Count('pk')
        ).order_by(
            'label'
        )
        serializer = StatisticsSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], url_name='statistics-by-group', detail=False)
    def statistics_by_group(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).values(
            label=F('part__cabinet__hardware__group__name')
        ).annotate(
            value=Count('pk')
        )
        serializer = StatisticsSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=['get'],
        url_name='statistics-by-tech-reason',
        detail=False
    )
    def statistics_by_tech_reason(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).values(
            label=F('technical_reasons__name')
        ).annotate(
            value=Count('pk')
        )
        serializer = StatisticsSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=['get'],
        url_name='statistics-by-org-reason',
        detail=False
    )
    def statistics_by_org_reason(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).values(
            label=F('organizational_reasons__name')
        ).annotate(
            value=Count('pk')
        )
        serializer = StatisticsSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=['get'],
        url_name='statistics-by-repair-method',
        detail=False
    )
    def statistics_by_repair_method(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).values(
            label=F('repair_method__name')
        ).annotate(
            value=Count('pk')
        )
        serializer = StatisticsSerializer(queryset, many=True)
        return Response(serializer.data)
