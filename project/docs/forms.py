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


class TextCreateForm(ModelForm):
    class Meta:
        model = Text
        fields = '__all__'


class TextUpdateForm(ModelForm):
    class Meta:
        model = Text
        exclude = ('protocol', 'slug')


class CharCreateForm(ModelForm):
    value = CharField(required=True)

    class Meta:
        model = Text
        fields = '__all__'


class CharUpdateForm(ModelForm):
    value = CharField(required=True)

    class Meta:
        model = Text
        exclude = ('protocol', 'slug')


class IntegerCreateForm(ModelForm):
    class Meta:
        model = Integer
        fields = '__all__'


class IntegerUpdateForm(ModelForm):
    class Meta:
        model = Integer
        exclude = ('protocol', 'slug')


class FloatCreateForm(ModelForm):
    class Meta:
        model = Float
        fields = '__all__'


class FloatUpdateForm(ModelForm):
    class Meta:
        model = Float
        exclude = ('protocol', 'slug')


class ImageForm(ModelForm):
    value = PreProcessingCSVFileField(label=_('Файл'), required=True)

    class Meta:
        model = File
        fields = '__all__'
