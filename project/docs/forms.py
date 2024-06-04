from django.forms import ModelForm
from django.forms.widgets import DateInput

from docs.models import ProtocolE2


class ProtocolE2Form(ModelForm):
    class Meta:
        model = ProtocolE2
        fields = '__all__'
        widgets = {
            'date': DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date'}
            ),
        }
