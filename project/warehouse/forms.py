from django.forms import (ChoiceField, DateInput, Form,
                          ModelForm, NumberInput, TextInput)

from staff.models import Dept
from warehouse.models import (ComponentStorage, Instrument, Material,
                              MaterialStorage, Storage)


class DeptForm(Form):
    dept = ChoiceField(label='Подразделение')

    def __init__(self, *args, **kwargs):
        super(DeptForm, self).__init__(*args, **kwargs)
        self.fields['dept'].choices = [
            (d.id, d.abbreviation) for d in Dept.objects.all()
        ]


class InstrumentForm(ModelForm):
    class Meta:
        model = Instrument
        exclude = ('owner', )
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Наименование'}),
            'inventory_number': TextInput(attrs={'placeholder': 'Инв. номер'}),
            'serial_number': TextInput(attrs={'placeholder': 'Зав. номер'}),
            'verification_period': NumberInput(attrs={'placeholder': 'Период проверки (месяцев)'}), # noqa (E501)
            'last_verification': DateInput(attrs={'placeholder': 'Дата послед. проверки'}), # noqa (E501)
        }


class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Наименование'}),
            'article_number': TextInput(attrs={'placeholder': 'Артикул'}),
            'measurement_unit': TextInput(attrs={'placeholder': 'Единицы измерения'}),
        }


class MaterialStorageForm(ModelForm):
    class Meta:
        model = MaterialStorage
        exclude = ('storage', )
        widgets = {
            'inventory_number': TextInput(attrs={'placeholder': 'Инв. номер'}),
            'amount': NumberInput(attrs={'placeholder': 'Количество'}),
        }


class ComponentStorageForm(ModelForm):
    class Meta:
        model = ComponentStorage
        exclude = ('storage', )
        widgets = {
            'inventory_number': TextInput(attrs={'placeholder': 'Инв. номер'}),
            'amount': NumberInput(attrs={'placeholder': 'Количество'}),
        }


class StorageForm(ModelForm):
    class Meta:
        model = Storage
        exclude = ('owner', )
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Наименование',
                    'autocomplete': 'off',
                }
            ),
        }
