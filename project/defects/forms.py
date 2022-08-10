from django import forms

from hardware.models import Connection, Facility


class DefectFilterForm(forms.Form):
    dispatch_object = forms.ChoiceField(label='Объект диспетчеризации')
    connection = forms.ChoiceField(label='Присоединение')

    def __init__(self, *args, **kwargs):
        super(DefectFilterForm, self).__init__(*args, **kwargs)
        self.fields['dispatch_object'].choices = [
            (d.id, d.abbreviation) for d in Facility.objects.all()
        ]
        self.fields['connection'].choices = [
            (c.id, c.abbreviation) for c in Connection.objects.all()
        ]
