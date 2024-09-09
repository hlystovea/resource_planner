import math

import pytest
from django.db.models import fields
from django_resized import ResizedImageField
from django.urls import reverse

from tests.common import get_field_context, search_field
from warehouse.forms import MaterialForm
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

        assert response.templates[0].name == 'warehouse/material_list.html', \
            'Проверьте, что используете шаблон material_list.html в ответе'
        assert 'material_list' in response.context, \
            'Проверьте, что передали поле "material_list" в контекст страницы'
        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'

        response = client.get(url, headers={'Hx-Request': True})
        assert response.templates[0].name == 'warehouse/includes/material_table.html', \
            'Проверьте, что используете шаблон material_table.html в ответе ' \
            'для htmx запроса'

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
            'Проверьте, что вместе с объектом Material передали поле ' \
            'типа MaterialStorage в контекст страницы'
        total = material_in_storage_1.amount + material_in_storage_2.amount
        assert math.isclose(material.total, total), \
            'Проверьте, что объект Material содержит поле total ' \
            'с общим количеством материала'

        response = client.get(url, headers={'Hx-Request': True})
        assert response.templates[0].name == 'warehouse/includes/material_row.html', \
            'Проверьте, что используете шаблон material_row.html в ответе ' \
            'для htmx запроса'

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

        assert response.templates[0].name == 'warehouse/material_detail.html', \
            'Проверьте, что используете шаблон material_detail.html в ответе'
        assert material is not None, \
            'Проверьте, что передали поле типа Material в контекст страницы'
        assert data['name'] == material.name, \
            'Проверьте, что сохраненный экземпляр `material` содержит ' \
            'соответствующее поле `name`'
        assert data['measurement_unit'] == material.measurement_unit, \
            'Проверьте, что измененный экземпляр `material` содержит ' \
            'соответствующее поле `measurement_unit`'

        headers = {'Hx-Request': True}
        response = client.post(url, follow=True, data=data, headers=headers)
        assert response.templates[0].name == 'warehouse/includes/material_row.html', \
            'Проверьте, что используете шаблон material_row.html в ответе ' \
            'для htmx запроса'

    @pytest.mark.django_db
    @pytest.mark.parametrize('name, unit', test_args)
    def test_material_view_update(self, name, unit, auto_login_user, material_1):
        client, user = auto_login_user()
        url = reverse('warehouse:material-update', kwargs={'pk': material_1.pk})

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], MaterialForm), \
            'Проверьте, что поле `form` содержит объект класса `MaterialForm`'
        assert 'is_update' in response.context, \
            'Проверьте, что передали поле `is_update` в контекст страницы'
        assert response.context['is_update'], \
            'Проверьте, что значение поля `is_update` в контексте стр. = `True`'

        response = client.get(url, headers={'Hx-Request': True})
        assert response.templates[0].name == 'warehouse/includes/material_inline_form.html', \
            'Проверьте, что используете шаблон material_inline_form.html в ответе ' \
            'для htmx запроса'

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
        
        material = Material.objects.create(name=name, measurement_unit=unit)
        url = reverse('warehouse:material-delete', kwargs={'pk': material.pk})
        response = client.delete(url, headers={'Hx-Request': True})

        assert response.status_code == 200
        assert len(response.content) == 0, \
            'Проверьте, что на htmx запрос возвращется пустой ответ'

    @pytest.mark.django_db
    def test_material_filters(
        self, client, material_in_storage_dept1, material_in_storage_dept2
    ):
        url = reverse('warehouse:material-list')
        materials = Material.objects.all()

        response = client.get(url)
        material_list = response.context['material_list']

        assert len(material_list) == len(materials), \
            'Проверьте, что без фильтрации передаются все объекты'

        response = client.get(f'{url}?dept={material_in_storage_dept1.storage.owner.pk}')
        material_list = response.context['material_list']

        assert material_in_storage_dept1.material in material_list, \
            'Фильтр по подразделению работает не правильно'
        assert material_in_storage_dept2.material not in material_list, \
            'Фильтр по подразделению работает не правильно'

        response = client.get(f'{url}?search={material_in_storage_dept1.material.name[-5:]}')
        material_list = response.context['material_list']

        assert material_in_storage_dept1.material in material_list, \
            'Поиск по подразделению работает не правильно'
        assert material_in_storage_dept2.material not in material_list, \
            'Поиск по подразделению работает не правильно'
