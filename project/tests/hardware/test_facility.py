import pytest

from django.db.models.fields import CharField
from django.urls import reverse

from hardware.models import Facility
from tests.common import get_field_context, search_field


class TestFacility:
    def test_facility_model(self):
        model_fields = Facility._meta.fields

        name_field = search_field(model_fields, 'name')
        assert name_field is not None, \
            'Модель Facility должна содержать поле name'
        assert isinstance(name_field, CharField), \
            'Поле name модели Facility должно быть текстовым CharField'
        assert not name_field.blank, \
            'Поле name модели Facility должно быть обязательным'

        abbreviation_field = search_field(model_fields, 'abbreviation')
        assert abbreviation_field is not None, \
            'Модель Facility должна содержать поле abbreviation'
        assert isinstance(abbreviation_field, CharField), \
            'Поле abbreviation модели Facility должно быть текстовым CharField'
        assert not abbreviation_field.blank, \
            'Поле abbreviation модели Facility должно быть обязательным'

    @pytest.mark.django_db
    def test_facility_view_get_detail(self, client, facility):
        try:
            url = reverse(
                'hardware:facility-detail', kwargs={'pk': facility.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200, \
            'Статус код страницы должен быть 200'
        assert response.templates[0].name == 'hardware/facility_detail.html', \
            'Проверьте, что используете шаблон facility_detail.html в ответе'

        facility = get_field_context(response.context, Facility)

        assert facility is not None, \
            'Проверьте, что передали поле типа `Facility` в контекст страницы'

    @pytest.mark.django_db
    def test_facility_view_get_li(self, client, facility):
        try:
            url = reverse(
                'hardware:facility-li', kwargs={'pk': facility.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200, \
            'Статус код страницы должен быть 200'
        assert response.templates[0].name == 'hardware/includes/menu_li.html', \
            'Проверьте, что используете шаблон menu_li.html в ответе'

        assert 'object' in response.context, \
            'Проверьте, что передали поле object в контекст страницы'
        assert isinstance(response.context['object'], Facility), \
            'Проверьте, что передали поле типа `Facility` в контекст страницы'

    @pytest.mark.django_db
    def test_facility_view_get_select(self, client):
        url = reverse('hardware:facility-select')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'facility_list' in response.context, \
            'Проверьте, что передали поле "facility_list" в контекст страницы'
        assert response.templates[0].name == 'hardware/includes/facility_select.html', \
            'Проверьте, что используете шаблон facility_select.html в ответе'
