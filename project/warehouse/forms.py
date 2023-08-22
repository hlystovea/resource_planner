from django.forms import ChoiceField, Form, ModelForm

from staff.models import Dept
from warehouse.models import Material, MaterialStorage


class DeptForm(Form):
    dept = ChoiceField(label='Подразделение')

    def __init__(self, *args, **kwargs):
        super(DeptForm, self).__init__(*args, **kwargs)
        self.fields['dept'].choices = [
            (d.id, d.abbreviation) for d in Dept.objects.all()
        ]


class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = '__all__'


class MaterialStorageForm(ModelForm):
    class Meta:
        model = MaterialStorage
        exclude = ['storage']
