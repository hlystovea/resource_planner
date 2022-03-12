from django import forms

from staff.models import Dept


class DeptForm(forms.Form):
    dept = forms.ChoiceField(label='Подразделение')

    def __init__(self, *args, **kwargs):
        super(DeptForm, self).__init__(*args, **kwargs)
        self.fields['dept'].choices = [
            (d.id, d.abbreviation) for d in Dept.objects.all()
        ]
