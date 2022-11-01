import pytest

from django.db.models import fields
from django.urls import reverse
from django_resized import ResizedImageField

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
