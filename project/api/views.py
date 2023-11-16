from django.db.models import Count, F, Value
from django.db.models.functions import Concat, ExtractYear
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from defects.filters import DefectFilter
from defects.models import Defect
from hardware.models import (Cabinet, Component, Connection,
                             Facility, Group, Hardware, Part)
from .serializers import (CabinetSerializer, ComponentSerializer,
                          ConnectionSerializer, DefectSerializer,
                          FacilitySerializer, GroupSerializer,
                          HardwareSerializer, PartSerializer,
                          StatisticsSerializer, YearSerializer)


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
        queryset = self.get_queryset().annotate(
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
        queryset = self.get_queryset().values(
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
        queryset = self.get_queryset().values(
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
        queryset = self.get_queryset().values(
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
        queryset = self.get_queryset().values(
            label=F('repair_method__name')
        ).annotate(
            value=Count('pk')
        )
        serializer = StatisticsSerializer(queryset, many=True)
        return Response(serializer.data)


class FacilityViewSet(ReadOnlyModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer

    @action(methods=['get'], url_name='connections', detail=True)
    def connections(self, request, *args, **kwargs):
        facility = get_object_or_404(Facility, pk=kwargs['pk'])
        queryset = facility.connections.annotate(
            facility_with_abbreviation=Concat(
                'facility__abbreviation', Value(' '), 'abbreviation'
            )
        )
        serializer = ConnectionSerializer(queryset, many=True)
        return Response(serializer.data)


class ConnectionViewSet(ReadOnlyModelViewSet):
    queryset = Connection.objects.annotate(
        facility_with_abbreviation=Concat(
            'facility__abbreviation', Value(' '), 'abbreviation'
        )
    )
    serializer_class = ConnectionSerializer

    @action(methods=['get'], url_name='hardware', detail=True)
    def hardware(self, request, *args, **kwargs):
        connection = get_object_or_404(Connection, pk=kwargs['pk'])
        serializer = HardwareSerializer(connection.hardware, many=True)
        return Response(serializer.data)


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    @action(methods=['get'], url_name='hardware', detail=True)
    def hardware(self, request, *args, **kwargs):
        group = get_object_or_404(Group, pk=kwargs['pk'])
        serializer = HardwareSerializer(group.hardware, many=True)
        return Response(serializer.data)


class HardwareViewSet(ReadOnlyModelViewSet):
    queryset = Hardware.objects.all()
    serializer_class = HardwareSerializer

    @action(methods=['get'], url_name='cabinets', detail=True)
    def cabinets(self, request, *args, **kwargs):
        hardware = get_object_or_404(Hardware, pk=kwargs['pk'])
        serializer = CabinetSerializer(hardware.cabinets, many=True)
        return Response(serializer.data)


class CabinetViewSet(ReadOnlyModelViewSet):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer

    @action(methods=['get'], url_name='parts', detail=True)
    def parts(self, request, *args, **kwargs):
        cabinet = get_object_or_404(Cabinet, pk=kwargs['pk'])
        queryset = cabinet.parts.annotate(
            name_with_component=Concat(
                'name', Value(' '), 'component__name'
            )
        )
        serializer = PartSerializer(queryset, many=True)
        return Response(serializer.data)


class PartViewSet(ReadOnlyModelViewSet):
    queryset = Part.objects.annotate(
        name_with_component=Concat(
            'name', Value(' '), 'component__name'
        )
    )
    serializer_class = PartSerializer

    @action(methods=['get'], url_name='parts', detail=True)
    def parts(self, request, *args, **kwargs):
        part = get_object_or_404(Part, pk=kwargs['pk'])
        queryset = part.parts.annotate(
            name_with_component=Concat(
                'name', Value(' '), 'component__name'
            )
        )
        serializer = PartSerializer(queryset, many=True)
        return Response(serializer.data)


class ComponentViewSet(ReadOnlyModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
