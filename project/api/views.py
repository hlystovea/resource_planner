from django.db.models import Value
from django.db.models.functions import Concat, ExtractYear
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from defects.models import Defect
from hardware.models import (Cabinet, Component, Connection,
                             Facility, Group, Hardware, Part)
from .serializers import (CabinetSerializer, ComponentSerializer,
                          ConnectionSerializer, DefectSerializer,
                          FacilitySerializer, GroupSerializer,
                          HardwareSerializer, PartSerializer, YearSerializer)


class DefectViewSet(ReadOnlyModelViewSet):
    queryset = Defect.objects.all()
    serializer_class = DefectSerializer

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


class FacilityViewSet(ReadOnlyModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer

    @action(methods=['get'], url_name='connections', detail=True)
    def connections(self, request, *args, **kwargs):
        facility = get_object_or_404(Facility, pk=kwargs['pk'])
        queryset = facility.connections.annotate(
            abbreviation_with_facility=Concat(
                'abbreviation', Value(' '), 'facility__abbreviation'
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

    @action(methods=['get'], url_name='components', detail=True)
    def components(self, request, *args, **kwargs):
        cabinet = get_object_or_404(Cabinet, pk=kwargs['pk'])
        serializer = ComponentSerializer(cabinet.components, many=True)
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
        serializer = PartSerializer(part.parts, many=True)
        return Response(serializer.data)


class ComponentViewSet(ReadOnlyModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

    @action(methods=['get'], url_name='parts', detail=True)
    def parts(self, request, *args, **kwargs):
        component = get_object_or_404(Component, pk=kwargs['pk'])
        serializer = PartSerializer(component.parts, many=True)
        return Response(serializer.data)
