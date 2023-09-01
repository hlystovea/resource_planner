import math
import pytest

from django.db.models import fields
from django_resized import ResizedImageField
from django.urls import reverse

from common import get_field_context, search_field
from warehouse.forms import DeptForm, MaterialForm
from warehouse.models import Material, MaterialStorage


class TestMaterial:
    test_args = [('some-name', 'unit'), ('foo', 'bar'), ('12', '11')]

    def test_material_model(self):
        model_fields = Material._meta.fields

        name_field = search_field(model_fields, 'name')
        assert name_field is not None, \
            'Модель Material должна содержать поле name'
        assert type(name_field) == fields.CharField, \
            'Поле name модели Material должно быть текстовым CharField'
        assert not name_field.blank, \
            'Поле name модели Material должно быть обязательным'

        measurement_unit_field = search_field(model_fields, 'measurement_unit')
        assert measurement_unit_field is not None, \
            'Модель Material должна содержать поле measurement_unit'
        assert type(measurement_unit_field) == fields.CharField, \
            'Поле measurement_unit должно быть текстовым CharField'
        assert not measurement_unit_field.blank, \
            'Поле measurement_unit должно быть обязательным'

        article_number_field = search_field(model_fields, 'article_number')
        assert article_number_field is not None, \
            'Модель Material должна содержать поле article_number'
        assert type(article_number_field) == fields.CharField, \
            'Поле article_number должно быть текстовым CharField'
        assert article_number_field.blank, \
            'Поле article_number не должно быть обязательным'

        image_field = search_field(model_fields, 'image')
        assert image_field is not None, \
            'Модель Material должна содержать поле image'
        assert type(image_field) == ResizedImageField, \
            'Поле image модели Material должно быть ResizedImageField'
        assert image_field.blank, \
            'Поле image модели Material не должно быть обязательным'

    @pytest.mark.django_db
    def test_material_view_get_list(self, client):
        try:
            url = reverse('warehouse:material-list')
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'material_list' in response.context, \
            'Проверьте, что передали поле "material_list" в контекст страницы'
        assert type(response.context.get('form')) == DeptForm, \
            'Проверьте, что передали поле типа DeptForm в контекст страницы'

    @pytest.mark.django_db
    def test_material_view_get_detail(
        self, client, material, material_in_storage_1, material_in_storage_2
    ):
        try:
            url = reverse(
                'warehouse:material-detail', kwargs={'pk': material.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200, \
            'Статус код страницы должен быть 200'

        material = get_field_context(response.context, Material)

        assert material is not None, \
            'Проверьте, что передали поле типа Material в контекст страницы'
        assert type(material.amount.first()) == MaterialStorage, \
            'Проверьте, что вместе с объектом Material передали поле' \
            'типа MaterialStorage в контекст страницы'
        total = material_in_storage_1.amount + material_in_storage_2.amount
        assert math.isclose(material.total, total), \
            'Проверьте, что объект Material содержит поле total' \
            'с общим количеством материала'

    @pytest.mark.django_db
    @pytest.mark.parametrize('name, unit', test_args)
    def test_material_view_create(self, name, unit, auto_login_user):
        client, user = auto_login_user()
        url = reverse('warehouse:material-create')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], MaterialForm), \
            'Проверьте, что поле `form` содержит объект класса `MaterialForm`'
        assert 'is_new' in response.context, \
            'Проверьте, что передали поле `is_new` в контекст страницы'
        assert response.context['is_new'], \
            'Проверьте, что значение поля `is_new` в контексте стр. = `True`'

        data = {
            'name': name,
            'measurement_unit': unit,
        }
        try:
            response = client.post(url, follow=True, data=data)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        material = get_field_context(response.context, Material)

        assert material is not None, \
            'Проверьте, что передали поле типа Material в контекст страницы'
        assert data['name'] == material.name, \
            'Проверьте, что сохраненный экземпляр `material` содержит' \
            'соответствующее поле `name`'
        assert data['measurement_unit'] == material.measurement_unit, \
            'Проверьте, что измененный экземпляр `material` содержит' \
            'соответствующее поле `measurement_unit`'

    @pytest.mark.django_db
    @pytest.mark.parametrize('name, unit', test_args)
    def test_material_view_update(self, name, unit, auto_login_user, material):
        client, user = auto_login_user()
        url = reverse('warehouse:material-update', kwargs={'pk': material.pk})

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], MaterialForm), \
            'Проверьте, что поле `form` содержит объект класса `MaterialForm`'

        data = {
            'name': name,
            'measurement_unit': unit,
        }
        try:
            response = client.post(url, follow=True, data=data)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        material = get_field_context(response.context, Material)

        assert material is not None, \
            'Проверьте, что передали поле типа Material в контекст страницы'
        assert data['name'] == material.name, \
            'Проверьте, что сохраненный экземпляр `material` содержит' \
            'соответствующее поле `name`'
        assert data['measurement_unit'] == material.measurement_unit, \
            'Проверьте, что измененный экземпляр `material` содержит' \
            'соответствующее поле `measurement_unit`'

    @pytest.mark.django_db
    @pytest.mark.parametrize('name, unit', test_args)
    def test_material_view_delete(self, name, unit, auto_login_user):
        client, user = auto_login_user()
        material = Material.objects.create(name=name, measurement_unit=unit)
        queryset = Material.objects.filter(name=name, measurement_unit=unit)

        assert queryset.exists(), \
            'Тест работает неправильно, экземпляр `material` отсутствует в БД'

        url = reverse('warehouse:material-delete', kwargs={'pk': material.pk})

        try:
            response = client.delete(url, follow=True)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert not queryset.exists(), \
            'Проверьте, что эксземпляр `material` удаляется из БД'
