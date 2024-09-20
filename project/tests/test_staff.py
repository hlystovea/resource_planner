import pytest

from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
from django.urls import reverse

from staff.models import Dept
from tests.common import search_field


class TestStaff:
    def test_dept_model(self):
        model_fields = Dept._meta.fields

        name_field = search_field(model_fields, 'name')
        assert name_field is not None, \
            'Модель Dept должна содержать поле name'
        assert isinstance(name_field, CharField), \
            'Поле name модели Dept должно быть текстовым CharField'
        assert not name_field.blank, \
            'Поле name модели Dept должно быть обязательным'

        abbreviation_field = search_field(model_fields, 'abbreviation')
        assert abbreviation_field is not None, \
            'Модель Dept должна содержать поле abbreviation'
        assert isinstance(abbreviation_field, CharField), \
            'Поле abbreviation модели Dept должно быть текстовым CharField'
        assert not abbreviation_field.blank, \
            'Поле abbreviation модели Dept должно быть обязательным'

        service_field = search_field(model_fields, 'service_id')
        assert service_field is not None, \
            'Модель Dept должна содержать поле service'
        assert isinstance(service_field, ForeignKey), \
            'Поле service модели Dept должно быть ForeignKey'
        assert service_field.blank, \
            'Поле service модели Dept не должно быть обязательным'

    @pytest.mark.django_db
    def test_dept_view_get_select(self, client):
        url = reverse('staff:dept-select')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'dept_list' in response.context, \
            'Проверьте, что передали поле "dept_list" в контекст страницы'
        assert response.templates[0].name == 'staff/dept_select.html', \
            'Проверьте, что используете шаблон dept_select.html в ответе'
