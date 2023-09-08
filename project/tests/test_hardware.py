import pytest

from django.db.models import fields
from django.urls import reverse

from hardware.forms import ComponentForm
from hardware.models import Component
from tests.common import get_field_context, search_field
from warehouse.forms import DeptForm
from warehouse.models import ComponentStorage


class TestComponent:
    test_args = ['some-name', 'foo_1', '12']

    def test_component_model(self):
        model_fields = Component._meta.fields

        name_field = search_field(model_fields, 'name')
        assert name_field is not None, \
            'Модель Component должна содержать поле name'
        assert type(name_field) == fields.CharField, \
            'Поле name модели Component должно быть текстовым CharField'
        assert not name_field.blank, \
            'Поле name модели Component должно быть обязательным'

        function_field = search_field(model_fields, 'function_id')
        assert function_field is not None, \
            'Модель Component должна содержать поле function'
        assert type(function_field) == fields.related.ForeignKey, \
            'Поле function должно быть ForeignKey'
        assert not function_field.blank, \
            'Поле function ндолжно быть обязательным'

        design_field = search_field(model_fields, 'design_id')
        assert design_field is not None, \
            'Модель Component должна содержать поле design'
        assert type(design_field) == fields.related.ForeignKey, \
            'Поле design должно быть ForeignKey'
        assert not design_field.blank, \
            'Поле design должно быть обязательным'

        repair_method_field = search_field(model_fields, 'repair_method_id')
        assert repair_method_field is not None, \
            'Модель Component должна содержать поле repair_method'
        assert type(repair_method_field) == fields.related.ForeignKey, \
            'Поле repair_method должно быть ForeignKey'
        assert not repair_method_field.blank, \
            'Поле repair_method должно быть обязательным'

        manufacturer_field = search_field(model_fields, 'manufacturer_id')
        assert manufacturer_field is not None, \
            'Модель Component должна содержать поле manufacturer'
        assert type(manufacturer_field) == fields.related.ForeignKey, \
            'Поле manufacturer должно быть ForeignKey'
        assert not manufacturer_field.blank, \
            'Поле manufacturer должно быть обязательным'

        type_field = search_field(model_fields, 'type')
        assert type_field is not None, \
            'Модель Component должна содержать поле type'
        assert type(type_field) == fields.CharField, \
            'Поле type должно быть CharField'
        assert type_field.blank, \
            'Поле type не должно быть обязательным'

        series_field = search_field(model_fields, 'series')
        assert series_field is not None, \
            'Модель Component должна содержать поле series'
        assert type(series_field) == fields.CharField, \
            'Поле series должно быть CharField'
        assert series_field.blank, \
            'Поле series не должно быть обязательным'

    @pytest.mark.django_db
    def test_component_view_get_list(self, client):
        url = reverse('hardware:component-list')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'component_list' in response.context, \
            'Проверьте, что передали поле "component_list" в контекст страницы'

        dept_form = get_field_context(response.context, DeptForm)
        assert dept_form is not None, \
            'Проверьте, что передали поле типа DeptForm в контекст страницы'

    @pytest.mark.django_db
    def test_component_view_get_detail(
        self, client, component, component_in_storage_1, component_in_storage_2
    ):
        try:
            url = reverse(
                'hardware:component-detail', kwargs={'pk': component.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200, \
            'Статус код страницы должен быть 200'

        component = get_field_context(response.context, Component)

        assert component is not None, \
            'Проверьте, что передали поле типа `Component` в контекст страницы'
        assert type(component.amount.first()) == ComponentStorage, \
            'Проверьте, что вместе с объектом Component передали поле ' \
            'типа ComponentStorage в контекст страницы'

        total = component_in_storage_1.amount + component_in_storage_2.amount
        assert component.total == total, \
            'Проверьте, что объект Component содержит поле total ' \
            'с общим количеством материала'

    @pytest.mark.django_db
    @pytest.mark.parametrize('name', test_args)
    def test_component_view_create(
        self, name, function, design, manufacturer, repair_method, auto_login_user
    ):
        client, user = auto_login_user()
        url = reverse('hardware:component-create')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        form = get_field_context(response.context, ComponentForm)
        assert form is not None, \
            'Проверьте, что передали поле типа `ComponentForm` в контекст стр.'

        assert 'is_new' in response.context, \
            'Проверьте, что передали поле `is_new` в контекст страницы'
        assert response.context['is_new'], \
            'Проверьте, что значение поля `is_new` в контексте стр. = `True`'

        data = {
            'name': name,
            'function': function,
            'design': design,
            'manufacturer': manufacturer,
            'repair_method': repair_method,
        }
        try:
            response = client.post(url, follow=True, data=data)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        component = get_field_context(response.context, Component)

        assert component is not None, \
            'Проверьте, что передали поле типа Component в контекст страницы'
        assert data['name'] == component.name, \
            'Проверьте, что сохраненный экземпляр `component` содержит' \
            'соответствующее поле `name`'

    @pytest.mark.django_db
    @pytest.mark.parametrize('name', test_args)
    def test_component_view_update(self, name, auto_login_user, component):
        client, user = auto_login_user()
        url = reverse('hardware:component-update', kwargs={'pk': component.pk})

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], ComponentForm), \
            'Проверьте, что поле `form` содержит объект класса `MaterialForm`'

        data = {
            'name': name,
        }
        try:
            response = client.post(url, follow=True, data=data)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        component = get_field_context(response.context, Component)

        assert component is not None, \
            'Проверьте, что передали поле типа Component в контекст страницы'
        assert data['name'] == component.name, \
            'Проверьте, что сохраненный экземпляр `component` содержит' \
            'соответствующее поле `name`'

    @pytest.mark.django_db
    @pytest.mark.parametrize('name', test_args)
    def test_component_view_delete(
        self, name, function, design, repair_method, auto_login_user
    ):
        client, user = auto_login_user()
        component = Component.objects.create(
            name=name,
            function=function,
            design=design,
            repair_method=repair_method
        )
        queryset = Component.objects.filter(name=name)

        assert queryset.exists(), \
            'Тест работает неправильно, экземпляр `component` отсутствует в БД'

        url = reverse('hardware:component-delete', kwargs={'pk': component.pk})

        try:
            response = client.delete(url, follow=True)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert not queryset.exists(), \
            'Проверьте, что эксземпляр `component` удаляется из БД'

    @pytest.mark.django_db
    def test_component_filters(
        self, client, component_in_storage_1, component_in_storage_2
    ):
        url = reverse('hardware:component-list')
        components = Component.objects.all()

        response = client.get(url)
        component_list = response.context['component_list']
        assert len(component_list) == len(components), \
            'Проверьте, что без фильтрации передаются все объекты'

        response = client.get(f'{url}?owner={component_in_storage_1.owner.pk}')
        component_list = response.context['component_list']
        assert component_in_storage_1.component in component_list, \
            'Фильтр по подразделению работает не правильно'
        assert component_in_storage_2.component not in component_list, \
            'Фильтр по подразделению работает не правильно'
