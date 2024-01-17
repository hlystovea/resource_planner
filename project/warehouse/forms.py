from django.forms import ChoiceField, Form, ModelForm

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


class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = '__all__'


class MaterialFormInline(ModelForm):
    class Meta:
        model = Material
        exclude = ('image', )


class MaterialStorageForm(ModelForm):
    class Meta:
        model = MaterialStorage
        exclude = ('storage', 'owner')


class ComponentStorageForm(ModelForm):
    class Meta:
        model = ComponentStorage
        exclude = ('storage', 'owner')


class StorageForm(ModelForm):
    class Meta:
        model = Storage
        fields = '__all__'


class StorageAddForm(ModelForm):
    class Meta:
        model = Storage
        exclude = ('parent_storage', )
