from django.forms import ModelForm
from django.forms.widgets import DateInput, CheckboxSelectMultiple, RadioSelect

from defects.models import Defect


class DefectForm(ModelForm):
    class Meta:
        model = Defect
        exclude = ('employee', )
        widgets = {
            'date': DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date'}
            ),
            'repair_date': DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date'}
            ),
            'features': CheckboxSelectMultiple,
            'condition': RadioSelect,
            'repair_method': RadioSelect,
        }
