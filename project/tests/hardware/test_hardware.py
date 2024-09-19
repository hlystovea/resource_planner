import pytest

from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
from django.urls import reverse

from hardware.models import Connection, Hardware
from tests.common import get_field_context, search_field


class TestHardware:
    def test_hardware_model(self):
        model_fields = Hardware._meta.fields

        name_field = search_field(model_fields, 'name')
        assert name_field is not None, \
            'Модель Connection должна содержать поле name'
        assert isinstance(name_field, CharField), \
            'Поле name модели Hardware должно быть текстовым CharField'
        assert not name_field.blank, \
            'Поле name модели Hardware должно быть обязательным'

        inventory_number_field = search_field(model_fields, 'inventory_number')
        assert inventory_number_field is not None, \
            'Модель Hardware должна содержать поле inventory_number'
        assert isinstance(inventory_number_field, CharField), \
            'Поле inventory_number модели Hardware должно быть текстовым CharField'
        assert not inventory_number_field.blank, \
            'Поле inventory_number модели Hardware должно быть обязательным'

        connection_field = search_field(model_fields, 'connection_id')
        assert connection_field is not None, \
            'Модель Hardware должна содержать поле connection'
        assert isinstance(connection_field, ForeignKey), \
            'Поле connection модели Hardware должно быть ForeignKey'
        assert not connection_field.blank, \
            'Поле connection модели Hardware должно быть обязательным'

        group_field = search_field(model_fields, 'group_id')
        assert group_field is not None, \
            'Модель Hardware должна содержать поле group'
        assert isinstance(group_field, ForeignKey), \
            'Поле group модели Hardware должно быть ForeignKey'
        assert not group_field.blank, \
            'Поле group модели Hardware должно быть обязательным'

    @pytest.mark.django_db
    def test_hardware_view_get_detail(self, client, hardware):
        try:
            url = reverse(
                'hardware:hardware-detail', kwargs={'pk': hardware.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200, \
            'Статус код страницы должен быть 200'
        assert response.templates[0].name == 'hardware/hardware_detail.html', \
            'Проверьте, что используете шаблон hardware_detail.html в ответе'

        hardware = get_field_context(response.context, Hardware)

        assert hardware is not None, \
            'Проверьте, что передали поле типа `Hardware` в контекст страницы'

    @pytest.mark.django_db
    def test_harwdare_view_get_li(self, client, hardware):
        try:
            url = reverse(
                'hardware:hardware-li', kwargs={'pk': hardware.id}
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
        assert isinstance(response.context['object'], Hardware), \
            'Проверьте, что передали поле типа `Hardware` в контекст страницы'

    @pytest.mark.django_db
    def test_hardware_view_get_ul(self, client, connection):
        try:
            url = reverse(
                'hardware:hardware-ul', kwargs={'pk': connection.id}
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
    def test_hardware_view_get_select(self, client):
        url = reverse('hardware:hardware-select')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'hardware_list' in response.context, \
            'Проверьте, что передали поле "hardware_list" в контекст страницы'
        assert response.templates[0].name == 'hardware/includes/hardware_select.html', \
            'Проверьте, что используете шаблон hardware_select.html в ответе'
