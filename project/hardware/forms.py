from django.forms import ModelForm, NumberInput, TextInput

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
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Услов. обозначение'}),
            'part': TextInput(attrs={'type': 'hidden'}),
            'cabinet': TextInput(attrs={'type': 'hidden'}),
            'release_year': NumberInput(attrs={'placeholder': 'Год выпуска'}),
            'launch_year': NumberInput(attrs={'placeholder': 'Год ввода'}),
            'comment': TextInput(attrs={'placeholder': 'Комментарий'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['aria-describedby'] = f'validation-{self[field_name].id_for_label}'  # noqa (E501)


class CabinetForm(ModelForm):
    field_order = ['abbreviation', 'name']

    class Meta:
        model = Cabinet
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Наименование'}),
            'abbreviation': TextInput(attrs={'placeholder': 'Опер. наименование'}),  # noqa (E501)
            'hardware': TextInput(attrs={'type': 'hidden'}),
            'series': TextInput(attrs={'placeholder': 'Серия'}),
            'type': TextInput(attrs={'placeholder': 'Тип'}),
            'release_year': NumberInput(attrs={'placeholder': 'Год выпуска'}),
            'launch_year': NumberInput(attrs={'placeholder': 'Год ввода'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['aria-describedby'] = f'validation-{self[field_name].id_for_label}'  # noqa (E501)
