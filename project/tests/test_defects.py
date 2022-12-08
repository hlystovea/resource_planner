import pytest

from django import forms
from django.db.models import fields
from django.urls import reverse
from django_resized import ResizedImageField
from sorl.thumbnail.fields import ImageFormField

from defects.forms import DefectForm
from defects.models import Defect, Effect
from staff.models import Employee


def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


def get_field_context(context, field_type):
    for field in context.keys():
        if field not in ('user', 'request') and type(context[field]) == field_type:
            return context[field]


class TestDefect:

    def test_defect_model(self):
        model_fields = Defect._meta.fields

        date_field = search_field(model_fields, 'date')
        assert date_field is not None, 'Модель Defect должна содержать поле "date"'
        assert type(date_field) == fields.DateField, \
            'Поле "date" модели Defect должно быть DateField'
        assert not date_field.blank, \
            'Поле "date" модели Defect должно быть обязательным'

        component_field = search_field(model_fields, 'component_id')
        assert component_field is not None, \
            'Модель Defect должна содержать поле "component"'
        assert type(component_field) == fields.related.ForeignKey, \
            'Поле "component" модели Defect должно быть ForeignKey'
        assert not component_field.blank, \
            'Поле "component" модели Defect должно быть обязательным'

        employee_field = search_field(model_fields, 'employee_id')
        assert employee_field is not None, \
            'Модель Defect должна содержать поле "employee"'
        assert type(employee_field) == fields.related.ForeignKey, \
            'Поле "employee" модели Defect должно быть ForeignKey'
        assert employee_field.related_model == Employee, \
            'Поле employee модели Defect должно быть ссылкой на модель Employee'
        assert not employee_field.blank, \
            'Поле "employee" модели Defect должно быть обязательным'

        description_field = search_field(model_fields, 'description')
        assert description_field is not None, \
            'Модель Defect должна содержать поле "description"'
        assert type(description_field) == fields.CharField, \
            'Поле description модели Defect должно быть текстовым CharField'
        assert not description_field.blank, \
            'Поле description модели Defect должно быть обязательным'

        image_field = search_field(model_fields, 'image')
        assert image_field is not None, \
            'Модель Defect должна содержать поле "image"'
        assert type(image_field) == ResizedImageField, \
            'Поле "image" модели Defect должно быть ResizedImageField'
        assert image_field.blank, \
            'Поле "image" модели Defect не должно быть обязательным'

        attachment_field = search_field(model_fields, 'attachment')
        assert attachment_field is not None, \
            'Модель Defect должна содержать поле "attachment"'
        assert type(attachment_field) == fields.files.FileField, \
            'Поле "attachment" модели Defect должно быть FileField'
        assert attachment_field.blank, \
            'Поле "attachment" модели Defect не должно быть обязательным'

    @pytest.mark.django_db
    def test_defect_view_get_list(self, client):
        try:
            url = reverse('defects:defect-list')
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200
        assert 'defect_list' in response.context, \
            'Проверьте, что передали поле "defect_list" в контекст страницы'

    @pytest.mark.django_db
    def test_defect_view_get_detail(self, client, defect):
        try:
            url = reverse(
                'defects:defect-detail', kwargs={'pk': defect.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200
        assert type(response.context.get('defect')) == Defect, \
            'Проверьте, что передали поле типа Defect в контекст страницы'

    @pytest.mark.django_db
    def test_defect_view_create(self, user_client):
        try:
            url = reverse('defects:defect-create')
            response = user_client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        if response.status_code in (301, 302):
            url = reverse('defects:defect-create')
            response = user_client.get(url)

        assert response.status_code != 404, \
            'Страница не найдена, проверьте этот адрес в *urls.py*'

        assert 'form' in response.context, \
            'Проверьте, что передали поле "form" в контекст страницы'
        assert len(response.context['form'].fields) == 12, \
            'Проверьте, что в форме "form" 12 полей'

        assert 'date' in response.context['form'].fields, \
            'Проверьте, что в форме "form" есть поле "date"'
        assert type(response.context['form'].fields['date']) == forms.fields.DateField, \
            'Проверьте, что в форме "form" поле "date" типа "DateField"'
        assert response.context['form'].fields['date'].required, \
            'Проверьте, что в форме "form" поле "date" обязательно'

        assert 'component' in response.context['form'].fields, \
            'Проверьте, что в форме "form" есть поле "component"'
        assert type(response.context['form'].fields['component']) == forms.models.ModelChoiceField, \
            'Проверьте, что в форме "form" поле "component" типа "ModelChoiceField"'
        assert response.context['form'].fields['component'].required, \
            'Проверьте, что в форме "form" поле "component" обязательно'

        assert not 'employee' in response.context['form'].fields, \
            'Проверьте, что в форме "form" нет поля "employee"'

        assert 'description' in response.context['form'].fields, \
            'Проверьте, что в форме "form" есть поле "description"'
        assert type(response.context['form'].fields['description']) == forms.fields.CharField, \
            'Проверьте, что в форме "form" поле "description" типа "CharField"'
        assert response.context['form'].fields['description'].required, \
            'Проверьте, что в форме "form" поле "description" обязательно'

        assert 'image' in response.context['form'].fields, \
            'Проверьте, что в форме "form" есть поле "image"'
        assert type(response.context['form'].fields['image']) == ImageFormField, \
            'Проверьте, что в форме "form" поле "image" типа "ResizedImageField"'
        assert not response.context['form'].fields['image'].required, \
            'Проверьте, что в форме "form" поле "image" не обязательно'

        assert 'effects' in response.context['form'].fields, \
            'Проверьте, что в форме "form" есть поле "effects"'
        assert type(response.context['form'].fields['effects']) == forms.models.ModelMultipleChoiceField, \
            'Проверьте, что в форме "form" поле "effects" типа "ModelMultipleChoiceField"'
        assert response.context['form'].fields['effects'].required, \
            'Проверьте, что в форме "form" поле "effects" обязательно'

        assert 'features' in response.context['form'].fields, \
            'Проверьте, что в форме "form" есть поле "features"'
        assert type(response.context['form'].fields['features']) == forms.models.ModelMultipleChoiceField, \
            'Проверьте, что в форме "form" поле "features" типа "ModelMultipleChoiceField"'
        assert response.context['form'].fields['features'].required, \
            'Проверьте, что в форме "form" поле "features" обязательно'

        assert 'condition' in response.context['form'].fields, \
            'Проверьте, что в форме "form" есть поле "condition"'
        assert type(response.context['form'].fields['condition']) == forms.models.ModelChoiceField, \
            'Проверьте, что в форме "form" поле "condition" типа "ModelChoiceField"'
        assert response.context['form'].fields['condition'].required, \
            'Проверьте, что в форме "form" поле "condition" обязательно'

        assert 'technical_reasons' in response.context['form'].fields, \
            'Проверьте, что в форме "form" есть поле "technical_reasons"'
        assert type(response.context['form'].fields['technical_reasons']) == forms.models.ModelMultipleChoiceField, \
            'Проверьте, что в форме "form" поле "technical_reasons" типа "ModelMultipleChoiceField"'
        assert not response.context['form'].fields['technical_reasons'].required, \
            'Проверьте, что в форме "form" поле "technical_reasons" не обязательно'

        assert 'organizational_reasons' in response.context['form'].fields, \
            'Проверьте, что в форме "form" есть поле "organizational_reasons"'
        assert type(response.context['form'].fields['organizational_reasons']) == forms.models.ModelMultipleChoiceField, \
            'Проверьте, что в форме "form" поле "organizational_reasons" типа "ModelMultipleChoiceField"'
        assert not response.context['form'].fields['organizational_reasons'].required, \
            'Проверьте, что в форме "form" поле "organizational_reasons" не обязательно'

        assert 'repair' in response.context['form'].fields, \
            'Проверьте, что в форме "form" есть поле "repair"'
        assert type(response.context['form'].fields['repair']) == forms.fields.CharField, \
            'Проверьте, что в форме "form" поле "repair" типа "CharField"'
        assert not response.context['form'].fields['repair'].required, \
            'Проверьте, что в форме "form" поле "repair" не обязательно'

        assert 'repair_date' in response.context['form'].fields, \
            'Проверьте, что в форме "form" есть поле "repair_date"'
        assert type(response.context['form'].fields['repair_date']) == forms.fields.DateField, \
            'Проверьте, что в форме "form" поле "repair_date" типа "DateField"'
        assert not response.context['form'].fields['repair_date'].required, \
            'Проверьте, что в форме "form" поле "repair_date" не обязательно'

        assert 'attachment' in response.context['form'].fields, \
            'Проверьте, что в форме "form" есть поле "attachment"'
        assert type(response.context['form'].fields['attachment']) == forms.fields.FileField, \
            'Проверьте, что в форме "form" поле "attachment" типа "FileField"'
        assert not response.context['form'].fields['attachment'].required, \
            'Проверьте, что в форме "form" поле "attachment" не обязательно'
