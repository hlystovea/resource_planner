from operator import truediv
from rest_framework.serializers import ModelSerializer, CharField

from hardware.models import (Cabinet, Component, Connection,
                             Facility, Group, Hardware)


class FacilitySerializer(ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'


class ConnectionSerializer(ModelSerializer):
    abbreviation_with_facility = CharField(read_only=True)

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


class ComponentSerializer(ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'
