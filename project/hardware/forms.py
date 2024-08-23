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
        fields = '__all__'
        widgets = {
            'hardware': TextInput(
                attrs={'type': 'hidden'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['aria-describedby'] = f'validation-{self[field_name].id_for_label}'  # noqa (E501)
