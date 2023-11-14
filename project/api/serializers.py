from rest_framework.serializers import (CharField, IntegerField, ListField,
                                        ModelSerializer, Serializer)

from defects.models import Defect
from hardware.models import (Cabinet, Component, Connection,
                             Facility, Group, Hardware, Part)


class DefectSerializer(ModelSerializer):
    class Meta:
        model = Defect
        fields = '__all__'


class YearSerializer(Serializer):
    years = ListField()


class StatisticsByYearSerializer(Serializer):
    year = IntegerField()
    defect_count = IntegerField()


class StatisticsByGroupSerializer(Serializer):
    group = CharField()
    defect_count = IntegerField()


class FacilitySerializer(ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'


class ConnectionSerializer(ModelSerializer):
    facility_with_abbreviation = CharField(read_only=True)

    class Meta:
        model = Connection
        fields = '__all__'


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class HardwareSerializer(ModelSerializer):
    class Meta:
        model = Hardware
        fields = '__all__'


class CabinetSerializer(ModelSerializer):
    class Meta:
        model = Cabinet
        fields = '__all__'


class PartSerializer(ModelSerializer):
    name_with_component = CharField(read_only=True)

    class Meta:
        model = Part
        fields = '__all__'


class ComponentSerializer(ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'
