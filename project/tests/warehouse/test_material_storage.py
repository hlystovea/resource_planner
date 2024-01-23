import pytest
from django.db.models import fields
from django.urls import reverse

from staff.models import Dept
from tests.common import get_field_context, search_field
from warehouse.models import Material, MaterialStorage, Storage
from warehouse.forms import MaterialStorageForm


class TestMaterialStorage:
    test_args = [('some-number', 12), ('foo', 12), ('123', 0)]

    def test_material_storage_model(self):
        model_fields = MaterialStorage._meta.fields

        material_field = search_field(model_fields, 'material_id')
        assert material_field is not None, \
            'Модель MaterialStorage должна содержать поле material'
        assert type(material_field) == fields.related.ForeignKey, \
            'Поле material модели MaterialStorage должно быть ссылкой ' \
            'на другую модель'
        assert material_field.related_model == Material, \
            'Поле material модели MaterialStorage должно быть ссылкой ' \
            'на модель Material'
        assert not material_field.blank, \
            'Поле material модели MaterialStorage должно быть обязательным'

        inventory_number_field = search_field(model_fields, 'inventory_number')
        assert inventory_number_field is not None, \
            'Модель MaterialStorage должна содержать поле inventory_number'
        assert type(inventory_number_field) == fields.CharField, \
            'Поле inventory_number должно быть текстовым CharField'
        assert inventory_number_field.blank, \
            'Поле inventory_number не должно быть обязательным'

        amount_field = search_field(model_fields, 'amount')
        assert amount_field is not None, \
            'Модель MaterialStorage должна содержать поле amount'
        assert type(amount_field) == fields.FloatField, \
            'Поле amount должно быть числовым FloatField'
        assert not amount_field.blank, \
            'Поле amount должно быть обязательным'

        owner_field = search_field(model_fields, 'owner_id')
        assert owner_field is not None, \
            'Модель MaterialStorage должна содержать поле owner'
        assert type(owner_field) == fields.related.ForeignKey, \
            'Поле owner должно быть ссылкой на другую модель'
        assert owner_field.related_model == Dept, \
            'Поле owner должно быть ссылкой на модель Dept'
        assert owner_field.blank, \
            'Поле owner не должно быть обязательным'

        storage_field = search_field(model_fields, 'storage_id')
        assert storage_field is not None, \
            'Модель MaterialStorage должна содержать поле storage'
        assert type(storage_field) == fields.related.ForeignKey, \
            'Поле storage должно быть ссылкой на другую модель'
        assert storage_field.related_model == Storage, \
            'Поле storage должно быть ссылкой на модель Storage'
        assert not storage_field.blank, \
            'Поле storage должно быть обязательным'

    @pytest.mark.django_db
    @pytest.mark.parametrize('number, amount', test_args)
    def test_material_storage_view_create(
        self, number, amount, material_1, storage_1, auto_login_user
    ):
        client, user = auto_login_user()
        url = reverse(
            'warehouse:material-storage-create',
            kwargs={'storage_pk': storage_1.pk}
        )

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], MaterialStorageForm), \
            'Проверьте, что поле `form` содержит форму `MaterialStorageForm`'

        data = {
            'material': material_1,
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
    def test_material_storage_view_update(
        self, number, amount, material_in_storage_1, auto_login_user
    ):
        client, user = auto_login_user()
        user.dept = material_in_storage_1.owner
        user.save()

        url = reverse(
            'warehouse:material-storage-update',
            kwargs={
                'storage_pk': material_in_storage_1.storage.pk,
                'pk': material_in_storage_1.pk,
            }
        )

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], MaterialStorageForm), \
            'Проверьте, что поле `form` содержит форму `MaterialStorageForm`'
        assert 'is_update' in response.context, \
            'Проверьте, что передали поле `is_update` в контекст стр.'
        assert response.context['is_update'], \
            'Проверьте, что значение поля `is_update` в контексте стр. = `True`'

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
    def test_storage_view_delete(
        self, number, amount, material, storage_1, auto_login_user
    ):
        client, user = auto_login_user()
        material_strg = MaterialStorage.objects.create(
            material=material,
            storage=storage_1,
            inventory_number=number,
            amount=amount
        )
        queryset = MaterialStorage.objects.filter(
            material=material,
            storage=storage_1,
            inventory_number=number,
            amount=amount
        )

        assert queryset.exists(), \
            'Тест работает неправильно, ' \
            'экземпляр `material_storage` отсутствует в БД'

        url = reverse(
            'warehouse:material-storage-delete',
            kwargs={
                'storage_pk': storage_1.pk,
                'pk': material_strg.pk,
            }
        )

        try:
            response = client.delete(url, follow=True)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert not queryset.exists(), \
            'Проверьте, что эксземпляр `material_storage` удаляется из БД'
