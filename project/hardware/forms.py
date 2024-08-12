from django.forms import ModelForm, TextInput

from hardware.models import Cabinet, Component, Manufacturer, Part


class ComponentForm(ModelForm):
    class Meta:
        model = Component
        fields = '__all__'


class ManufacturerForm(ModelForm):
    class Meta:
        model = Manufacturer
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Введите наименование..',
                    'autofocus': '',
                }
            ),
        }


class PartForm(ModelForm):
    class Meta:
        model = Part
        fields = '__all__'


class CabinetForm(ModelForm):
    class Meta:
        model = Cabinet
        exclude = ('hardware', )
