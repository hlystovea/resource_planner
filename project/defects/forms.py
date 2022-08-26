from django.forms import ChoiceField, ModelForm, Form
from django.forms.widgets import DateInput, TextInput, CheckboxSelectMultiple
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from defects.models import Defect
from hardware.models import Cabinet, Connection, Facility, Hardware


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
    facility = ChoiceField(label=_('Объект диспетчеризации'))
    connection = ChoiceField(label=_('Присоединение'))
    hardware = ChoiceField(label=_('Оборудование'))
    cabinet = ChoiceField(label=_('Шкаф/панель'))

    def __init__(self, *args, **kwargs):
        super(DefectFilterForm, self).__init__(*args, **kwargs)

        facilities = Facility.objects.all()
        connections = Connection.objects.all()
        hardware = Hardware.objects.all()
        cabinets = Cabinet.objects.all()
    
        query_dict = args[0]

        if query_dict:
            if query_dict.get('facility'):
                connections = connections.filter(facility=query_dict.get('facility')[0])
            if query_dict.get('connection'):
                hardware = hardware.filter(connection=query_dict.get('connection')[0])
            if query_dict.get('hardware'):
                cabinets = cabinets.filter(hardware=query_dict.get('hardware')[0])

        self.fields['facility'].choices = facilities.values_list('id', 'abbreviation')
        self.fields['connection'].choices = connections.values_list('id', 'abbreviation')
        self.fields['hardware'].choices = hardware.values_list('id', 'name')
        self.fields['cabinet'].choices = cabinets.values_list('id', 'abbreviation')
