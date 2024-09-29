from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import ModelForm, FileField
from django.forms.widgets import DateInput
from django.utils.translation import gettext_lazy as _
from pandas.errors import EmptyDataError

from docs.models import File, Protocol, ProtocolE2, Text
from docs.utils import plot_from_csv


LABELS = {
    'file_1': _('Осциллограмма процесса возбуждения ВГ на АРВ1'),
    'file_2': _('Осциллограмма процесса возбуждения ВГ на АРВ2'),
    'file_3': _('Осциллограмма процесса гашения ТП ВГ на АРВ1'),
    'file_4': _('Осциллограмма процесса гашения ТП ВГ на АРВ2'),
    'file_5': _('Осциллограмма процесса возбуждения ГГ на АРВ1 в режиме (Ug)'),
    'file_6': _('Осциллограмма процесса возбуждения ГГ на АРВ2 в режиме (Ug)'),
    'file_7': _('Осциллограмма процесса возбуждения ГГ на АРВ1 в режиме (If)'),
    'file_8': _('Осциллограмма процесса возбуждения ГГ на АРВ2 в режиме (If)'),
    'file_9': _('Осциллограмма процесса гашения ГГ на АРВ1'),
    'file_10': _('Осциллограмма процесса гашения ГГ на АРВ2'),
}


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


class ProtocolE2Form(ModelForm):
    file_1 = PreProcessingCSVFileField(label=LABELS['file_1'], required=True)
    file_2 = PreProcessingCSVFileField(label=LABELS['file_2'], required=True)
    file_3 = PreProcessingCSVFileField(label=LABELS['file_3'], required=True)
    file_4 = PreProcessingCSVFileField(label=LABELS['file_4'], required=True)
    file_5 = PreProcessingCSVFileField(label=LABELS['file_5'], required=True)
    file_6 = PreProcessingCSVFileField(label=LABELS['file_6'], required=True)
    file_7 = PreProcessingCSVFileField(label=LABELS['file_7'], required=True)
    file_8 = PreProcessingCSVFileField(label=LABELS['file_8'], required=True)
    file_9 = PreProcessingCSVFileField(label=LABELS['file_9'], required=True)
    file_10 = PreProcessingCSVFileField(label=LABELS['file_10'], required=True)

    class Meta:
        model = ProtocolE2
        fields = '__all__'
        widgets = {
            'date': DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date'}
            ),
        }


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


class ImageForm(ModelForm):
    class Meta:
        model = File
        fields = '__all__'
