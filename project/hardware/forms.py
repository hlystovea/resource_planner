from django.forms import ModelForm

from hardware.models import Component, Manufacturer


class ComponentForm(ModelForm):
    class Meta:
        model = Component
        fields = '__all__'


class ManufacturerForm(ModelForm):
    class Meta:
        model = Manufacturer
        fields = '__all__'
