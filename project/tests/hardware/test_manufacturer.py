import pytest

from django.db.models.fields import CharField
from django.urls import reverse

from hardware.forms import ManufacturerForm
from hardware.models import Manufacturer
from tests.common import search_field


class TestManufacturer:
    def test_manufacturer_model(self):
        model_fields = Manufacturer._meta.fields

        name_field = search_field(model_fields, 'name')
        assert name_field is not None, \
            'Модель Manufacturer должна содержать поле name'
        assert isinstance(name_field, CharField), \
            'Поле name модели Manufacturer должно быть текстовым CharField'
        assert not name_field.blank, \
            'Поле name модели Manufacturer должно быть обязательным'

    @pytest.mark.django_db
    def test_manufacturer_input(self, auto_login_user):
        client, _ = auto_login_user()
        url = reverse('hardware:manufacturer-input')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], ManufacturerForm), \
            'Проверьте, что поле `form` содержит объект класса `ManufacturerForm`'
        assert response.templates[0].name == 'hardware/includes/manufacturer_input.html', \
            'Проверьте, что используете шаблон manufacturer_input.html в ответе'

        data = {
            'name': 'some',
        }

        try:
            response = client.post(url, data=data, follow=True)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'selected_manufacturer' in response.context, \
            'Проверьте, что передали поле `selected_manufacturer` в контекст страницы'
        assert 'manufacturer_list' in response.context, \
            'Проверьте, что передали поле `manufacturer_list` в контекст страницы'
        assert response.templates[0].name == 'hardware/includes/manufacturer_select.html', \
            'Проверьте, что используете шаблон manufacturer_select.html в ответе'
        assert Manufacturer.objects.filter(name=data['name']).exists(), \
            'Проверьте, что происходит сохранение нового экземпляра `Manufacturer`'

    @pytest.mark.django_db
    def test_manufacturer_view_get_select(self, client):
        url = reverse('hardware:manufacturer-select')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'manufacturer_list' in response.context, \
            'Проверьте, что передали поле "manufacturer_list" в контекст страницы'
        assert response.templates[0].name == 'hardware/includes/manufacturer_select.html', \
            'Проверьте, что используете шаблон manufacturer_select.html в ответе'

    @pytest.mark.django_db
    def test_manufacturer_view_get_options(self, client):
        url = reverse('hardware:manufacturer-options')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'manufacturer_list' in response.context, \
            'Проверьте, что передали поле "manufacturer_list" в контекст страницы'
        assert response.templates[0].name == 'hardware/includes/manufacturer_options.html', \
            'Проверьте, что используете шаблон manufacturer_options.html в ответе'
