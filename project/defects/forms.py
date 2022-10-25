from django.forms import ModelForm
from django.forms.widgets import DateInput
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from defects.models import Defect


class DefectForm(ModelForm):
    class Meta:
        model = Defect
        exclude = ('employee', )
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
