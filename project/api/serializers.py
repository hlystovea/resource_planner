from rest_framework.serializers import (CharField, IntegerField, ListField,
                                        ModelSerializer, Serializer)

from defects.models import Defect


class DefectSerializer(ModelSerializer):
    class Meta:
        model = Defect
        fields = '__all__'


class YearSerializer(Serializer):
    years = ListField()


class StatisticsSerializer(Serializer):
    label = CharField()
    value = IntegerField()
