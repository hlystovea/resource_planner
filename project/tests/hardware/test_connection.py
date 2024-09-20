import pytest

from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
from django.urls import reverse

from hardware.models import Connection
from tests.common import get_field_context, search_field


class TestConnection:
    def test_connection_model(self):
        model_fields = Connection._meta.fields

        name_field = search_field(model_fields, 'name')
        assert name_field is not None, \
            'Модель Connection должна содержать поле name'
        assert isinstance(name_field, CharField), \
            'Поле name модели Connection должно быть текстовым CharField'
        assert not name_field.blank, \
            'Поле name модели Connection должно быть обязательным'

        abbreviation_field = search_field(model_fields, 'abbreviation')
        assert abbreviation_field is not None, \
            'Модель Connection должна содержать поле abbreviation'
        assert isinstance(abbreviation_field, CharField), \
            'Поле abbreviation модели Connection должно быть текстовым CharField'
        assert not abbreviation_field.blank, \
            'Поле abbreviation модели Connection должно быть обязательным'

        facility_field = search_field(model_fields, 'facility_id')
        assert facility_field is not None, \
            'Модель Connection должна содержать поле facility'
        assert isinstance(facility_field, ForeignKey), \
            'Поле facility модели Connection должно быть ForeignKey'
        assert not facility_field.blank, \
            'Поле facility модели Connection должно быть обязательным'

    @pytest.mark.django_db
    def test_connection_view_get_detail(self, client, connection):
        try:
            url = reverse(
                'hardware:connection-detail', kwargs={'pk': connection.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200, \
            'Статус код страницы должен быть 200'
        assert response.templates[0].name == 'hardware/connection_detail.html', \
            'Проверьте, что используете шаблон connection_detail.html в ответе'

        connection = get_field_context(response.context, Connection)

        assert connection is not None, \
            'Проверьте, что передали поле типа `Connection` в контекст страницы'

    @pytest.mark.django_db
    def test_connection_view_get_li(self, client, connection):
        try:
            url = reverse(
                'hardware:connection-li', kwargs={'pk': connection.id}
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
        assert isinstance(response.context['object'], Connection), \
            'Проверьте, что передали поле типа `Connection` в контекст страницы'

    @pytest.mark.django_db
    def test_connection_view_get_ul(self, client, connection):
        try:
            url = reverse(
                'hardware:connection-ul', kwargs={'pk': connection.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200, \
            'Статус код страницы должен быть 200'
        assert response.templates[0].name == 'hardware/includes/menu_ul.html', \
            'Проверьте, что используете шаблон menu_ul.html в ответе'

        assert 'object' in response.context, \
            'Проверьте, что передали поле "object" в контекст страницы'
        assert isinstance(response.context['object'], Connection), \
            'Проверьте, что передали поле типа `Connection` в контекст страницы'

    @pytest.mark.django_db
    def test_connection_view_get_select(self, client):
        url = reverse('hardware:connection-select')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'connection_list' in response.context, \
            'Проверьте, что передали поле "connection_list" в контекст страницы'
        assert response.templates[0].name == 'hardware/includes/connection_select.html', \
            'Проверьте, что используете шаблон connection_select.html в ответе'
