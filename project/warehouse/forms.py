from django.forms import ChoiceField, Form, ModelForm, TextInput

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


class InstrumentInlineForm(ModelForm):
    class Meta:
        model = Instrument
        exclude = ('owner', 'image')
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Наименование'}),
            'inventory_number': TextInput(attrs={'placeholder': 'Инв. номер'}),
            'serial_number': TextInput(attrs={'placeholder': 'Зав. номер'}),
        }


class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = '__all__'


class MaterialInlineForm(ModelForm):
    class Meta:
        model = Material
        exclude = ('image', )
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Наименование'}),
            'article_number': TextInput(attrs={'placeholder': 'Артикул'}),
            'measurement_unit': TextInput(attrs={'placeholder': 'Единицы измерения'}),
        }


class MaterialStorageForm(ModelForm):
    class Meta:
        model = MaterialStorage
        exclude = ('storage', )


class ComponentStorageForm(ModelForm):
    class Meta:
        model = ComponentStorage
        exclude = ('storage', )


class StorageForm(ModelForm):
    class Meta:
        model = Storage
        exclude = ('parent_storage', 'owner')
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Наименование'}),
        }
