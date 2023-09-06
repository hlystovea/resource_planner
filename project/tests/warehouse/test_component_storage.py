import pytest
from django.db.models import fields
from django.urls import reverse

from hardware.models import Component
from staff.models import Dept
from tests.common import get_field_context, search_field
from warehouse.forms import ComponentStorageForm
from warehouse.models import ComponentStorage, Storage


class TestComponentStorage:
    test_args = [('some-number', 12), ('foo', 12), ('123', 0)]

    def test_component_storage_model(self):
        model_fields = ComponentStorage._meta.fields

        component_field = search_field(model_fields, 'component_id')
        assert component_field is not None, \
            'Модель ComponentStorage должна содержать поле component'
        assert type(component_field) == fields.related.ForeignKey, \
            'Поле component модели ComponentStorage должно быть ссылкой ' \
            'на другую модель'
        assert component_field.related_model == Component, \
            'Поле component модели ComponentStorage должно быть ссылкой ' \
            'на модель Component'
        assert not component_field.blank, \
            'Поле component модели ComponentStorage должно быть обязательным'

        inventory_number_field = search_field(model_fields, 'inventory_number')
        assert inventory_number_field is not None, \
            'Модель ComponentStorage должна содержать поле inventory_number'
        assert type(inventory_number_field) == fields.CharField, \
            'Поле inventory_number должно быть текстовым CharField'
        assert inventory_number_field.blank, \
            'Поле inventory_number не должно быть обязательным'

        amount_field = search_field(model_fields, 'amount')
        assert amount_field is not None, \
            'Модель ComponentStorage должна содержать поле amount'
        assert type(amount_field) == fields.PositiveSmallIntegerField, \
            'Поле amount должно быть числовым PositiveSmallIntegerField'
        assert not amount_field.blank, \
            'Поле amount должно быть обязательным'

        owner_field = search_field(model_fields, 'owner_id')
        assert owner_field is not None, \
            'Модель ComponentStorage должна содержать поле owner'
        assert type(owner_field) == fields.related.ForeignKey, \
            'Поле owner должно быть ссылкой на другую модель'
        assert owner_field.related_model == Dept, \
            'Поле owner должно быть ссылкой на модель Dept'
        assert owner_field.blank, \
            'Поле owner не должно быть обязательным'

        storage_field = search_field(model_fields, 'storage_id')
        assert storage_field is not None, \
            'Модель ComponentStorage должна содержать поле storage'
        assert type(storage_field) == fields.related.ForeignKey, \
            'Поле storage должно быть ссылкой на другую модель'
        assert storage_field.related_model == Storage, \
            'Поле storage должно быть ссылкой на модель Storage'
        assert not storage_field.blank, \
            'Поле storage должно быть обязательным'

    @pytest.mark.django_db
    @pytest.mark.parametrize('number, amount', test_args)
    def test_component_storage_view_create(
        self, number, amount, component, storage_1, auto_login_user
    ):
        client, user = auto_login_user()
        url = reverse(
            'warehouse:component-storage-create',
            kwargs={'storage_pk': storage_1.pk}
        )

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], ComponentStorageForm), \
            'Проверьте, что поле `form` содержит форму `ComponentStorageForm`'
        assert 'is_new' in response.context, \
            'Проверьте, что передали поле `is_new` в контекст стр.'
        assert response.context['is_new'], \
            'Проверьте, что значение поля `is_new` в контексте стр. = `True`'

        data = {
            'component': component,
            'inventory_number': number,
            'amount': amount,
        }
        try:
            response = client.post(url, follow=True, data=data)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        storage = get_field_context(response.context, Storage)

        assert storage is not None, \
            'Проверьте, что передали поле `storage` в контекст страницы'

    @pytest.mark.django_db
    @pytest.mark.parametrize('number, amount', test_args)
    def test_component_storage_view_update(
        self, number, amount, component_in_storage_1, auto_login_user
    ):
        client, user = auto_login_user()
        user.dept = component_in_storage_1.owner
        user.save()

        url = reverse(
            'warehouse:component-storage-update',
            kwargs={
                'storage_pk': component_in_storage_1.storage.pk,
                'pk': component_in_storage_1.pk,
            }
        )

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], ComponentStorageForm), \
            'Проверьте, что поле `form` содержит форму `MaterialStorageForm`'

        data = {
            'inventory_number': number,
            'amount': amount,
        }

        try:
            response = client.post(url, follow=True, data=data)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        storage = get_field_context(response.context, Storage)

        assert storage is not None, \
            'Проверьте, что передали поле `storage` в контекст страницы'

    @pytest.mark.django_db
    @pytest.mark.parametrize('number, amount', test_args)
    def test_component_view_delete(
        self, number, amount, component, storage_1, auto_login_user
    ):
        client, user = auto_login_user()
        component_storage = ComponentStorage.objects.create(
            component=component,
            storage=storage_1,
            inventory_number=number,
            amount=amount
        )
        queryset = ComponentStorage.objects.filter(
            component=component,
            storage=storage_1,
            inventory_number=number,
            amount=amount
        )

        assert queryset.exists(), \
            'Тест работает неправильно, ' \
            'экземпляр `component_storage` отсутствует в БД'

        url = reverse(
            'warehouse:component-storage-delete',
            kwargs={
                'storage_pk': storage_1.pk,
                'pk': component_storage.pk,
            }
        )

        try:
            response = client.delete(url, follow=True)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert not queryset.exists(), \
            'Проверьте, что эксземпляр `material_storage` удаляется из БД'
