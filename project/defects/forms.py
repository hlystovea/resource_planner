from django.forms import ChoiceField, ModelForm, Form
from django.forms.widgets import DateInput
from django.utils.timezone import now

from defects.models import Defect
from hardware.models import Connection, Facility


class DefectForm(ModelForm):
    class Meta:
        model = Defect
        fields = '__all__'
        widgets = {
            'date': DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date', 'max': now().date().isoformat()}
            ),
            'repair_date': DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date', 'max': now().date().isoformat()}
            )
        }


class DefectFilterForm(Form):
    dispatch_object = ChoiceField(label='Объект диспетчеризации')
    connection = ChoiceField(label='Присоединение')

    def __init__(self, *args, **kwargs):
        super(DefectFilterForm, self).__init__(*args, **kwargs)
        self.fields['dispatch_object'].choices = [
            (d.id, d.abbreviation) for d in Facility.objects.all()
        ]
        self.fields['connection'].choices = [
            (c.id, c.abbreviation) for c in Connection.objects.all()
        ]
