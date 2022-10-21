from rest_framework.serializers import ModelSerializer

from hardware.models import (Cabinet, Component, Connection,
                             Facility, Group, Hardware)


class FacilitySerializer(ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'


class ConnectionSerializer(ModelSerializer):
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
