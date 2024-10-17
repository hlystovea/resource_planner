from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import CharField, FileField, ModelForm
from django.forms.widgets import DateInput
from django.utils.translation import gettext_lazy as _
from pandas.errors import EmptyDataError

from docs.models import File, Float, Integer, Protocol, Text
from docs.utils import plot_from_csv


class PreProcessingCSVFileField(FileField):
    def clean(self, data: InMemoryUploadedFile, initial=None):
        if data.name.endswith('csv'):
            try:
                data.file = plot_from_csv(data.file)
                data.name = f'{data.name}.png'
            except EmptyDataError:
                raise ValidationError(
                    self.error_messages['empty'], code='empty')
        return super().clean(data, initial)


class ProtocolForm(ModelForm):
    class Meta:
        model = Protocol
        fields = '__all__'
        widgets = {
            'date': DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date'}
            ),
        }


class TextForm(ModelForm):
    class Meta:
        model = Text
        fields = '__all__'


class CharForm(ModelForm):
    value = CharField(required=True)

    class Meta:
        model = Text
        fields = '__all__'


class IntegerForm(ModelForm):
    class Meta:
        model = Integer
        fields = '__all__'


class FloatForm(ModelForm):
    class Meta:
        model = Float
        fields = '__all__'


class ImageForm(ModelForm):
    value = PreProcessingCSVFileField(label=_('Файл'), required=True)

    class Meta:
        model = File
        fields = '__all__'
