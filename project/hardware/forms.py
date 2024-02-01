from django.forms import CharField, ChoiceField, ModelForm, TextInput

from hardware.models import Component, Manufacturer
from staff.models import Dept


class ListTextWidget(TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list':'list__%s' % self._name})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name

        for item in self._list:
            data_list += '<option value="%s">' % item
        data_list += '</datalist>'

        return (text_html + data_list)


class ComponentForm(ModelForm):
    manufacturer = CharField(required=True)

    def __init__(self, *args, **kwargs):
        _manufacturer_list = Manufacturer.objects.values_list(
            'name', flat=True).order_by('name')
        super(ComponentForm, self).__init__(*args, **kwargs)
        self.fields['manufacturer'].widget = ListTextWidget(
            data_list=_manufacturer_list,
            name='manufacturer-list'
        )

    def clean(self):
        cleaned_data = self.cleaned_data

        try:
            manufacturer = Manufacturer.objects.get(
                name=cleaned_data['manufacturer']
            )
        except Manufacturer.DoesNotExist:
            manufacturer = Manufacturer.objects.create(
                name=cleaned_data['manufacturer']
            )

        cleaned_data['manufacturer'] = manufacturer
        return cleaned_data

    class Meta:
        model = Component
        fields = '__all__'


class ComponentFilterForm(ModelForm):
    dept = ChoiceField(label='Подразделение')

    def __init__(self, *args, **kwargs):
        super(ComponentFilterForm, self).__init__(*args, **kwargs)
        self.fields['dept'].choices = [
            (d.id, d.abbreviation) for d in Dept.objects.all()
        ]

    class Meta:
        model = Component
        fields = ('dept', 'manufacturer')
