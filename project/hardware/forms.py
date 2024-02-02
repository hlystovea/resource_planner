from django.forms import ChoiceField, ModelForm

from hardware.models import Component
from staff.models import Dept


class ComponentForm(ModelForm):
    class Meta:
        model = Component
        fields = '__all__'


class ComponentFilterForm(ModelForm):
    dept = ChoiceField(label='Подразделение')

    class Meta:
        model = Component
        fields = ('dept', 'manufacturer')

    def __init__(self, *args, **kwargs):
        super(ComponentFilterForm, self).__init__(*args, **kwargs)
        self.fields['dept'].choices = [
            (d.id, d.abbreviation) for d in Dept.objects.all()
        ]
