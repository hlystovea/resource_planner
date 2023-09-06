from django.forms import ModelForm

from hardware.models import Component


class ComponentForm(ModelForm):
    class Meta:
        model = Component
        fields = '__all__'
