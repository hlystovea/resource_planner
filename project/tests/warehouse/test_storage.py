import pytest
from django.db.models import fields
from django.urls import reverse
from qr_code.qrcode.utils import QRCodeOptions

from tests.common import get_field_context, search_field
from staff.models import Dept
from warehouse.forms import (ComponentStorageForm, MaterialStorageForm,
                             StorageForm)
from warehouse.models import Storage


class TestStorage:
    test_args = ['some-name', 'foo', '12']

    def test_storage_model(self):
        model_fields = Storage._meta.fields

        name_field = search_field(model_fields, 'name')
        assert name_field is not None, \
            'Модель Storage должна содержать поле name'
        assert type(name_field) == fields.CharField, \
            'Поле name модели Storage должно быть текстовым CharField'
        assert not name_field.blank, \
            'Поле name модели Storage должно быть обязательным'

        parent_storage_field = search_field(model_fields, 'parent_storage_id')
        assert parent_storage_field is not None, \
            'Модель Storage должна содержать поле parent_storage'
        assert type(parent_storage_field) == fields.related.ForeignKey, \
            'Поле parent_storage должно быть ссылкой на другую модель'
        assert parent_storage_field.related_model == Storage, \
            'Поле parent_storage должно быть ссылкой на модель Storage'
        assert parent_storage_field.blank, \
            'Поле parent_storage модели Storage не должно быть обязательным'

        owner_field = search_field(model_fields, 'owner_id')
        assert owner_field is not None, \
            'Модель Storage должна содержать поле owner'
        assert type(owner_field) == fields.related.ForeignKey, \
            'Поле owner должно быть ссылкой на другую модель'
        assert owner_field.related_model == Dept, \
            'Поле owner должно быть ссылкой на модель Dept'
        assert owner_field.blank, \
            'Поле owner не должно быть обязательным'

    @pytest.mark.django_db
    def test_storage_view_get_qrcode(self, client, storage_1):
        try:
            url = reverse(
                'warehouse:storage-qrcode', kwargs={'pk': storage_1.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200
        assert type(response.context.get('storage')) == Storage, \
            'Проверьте, что передали поле типа Storage в контекст страницы'
        assert type(response.context.get('qr_options')) == QRCodeOptions, \
            'Проверьте, что передали поле типа QRCodeOptions в контекст стр.'
        assert 'storage_url' in response.context, \
            'Проверьте, что передали поле "storage_url" в контекст страницы'
        assert 'internal_storage_urls' in response.context, \
            'Проверьте, что передали поле "internal_storage_urls" в контекст стр.'  # noqa (E501)

    @pytest.mark.django_db
    def test_storage_view_get_list(self, client, storage_1):
        try:
            url = reverse('warehouse:storage-list')
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert response.templates[0].name == 'warehouse/storage_list.html', \
            'Проверьте, что используете шаблон storage_list.html в ответе'

        assert 'storage_list' in response.context, \
            'Проверьте, что передали поле "storage_list" в контекст страницы'

    @pytest.mark.django_db
    def test_storage_view_get_detail(self, client, storage_1):
        try:
            url = reverse(
                'warehouse:storage-detail', kwargs={'pk': storage_1.pk}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert response.templates[0].name == 'warehouse/storage_detail.html', \
            'Проверьте, что используете шаблон storage_detail.html в ответе'

        storage_from_context = get_field_context(response.context, Storage)
        assert storage_from_context is not None, \
            'Проверьте, что передали поле типа Storage в контекст страницы'

        materialstorage_form = get_field_context(
            response.context, MaterialStorageForm)
        assert materialstorage_form is not None, \
            'Проверьте, что передали поле типа MaterialStorageForm ' \
            'в контекст страницы'

        componentstorage_form = get_field_context(
            response.context, ComponentStorageForm)
        assert componentstorage_form is not None, \
            'Проверьте, что передали поле типа ComponentStorageForm ' \
            'в контекст страницы'

        response = client.get(url, headers={'Hx-Request': True})
        assert response.templates[0].name == 'warehouse/includes/storage_content.html', \
            'Проверьте, что используете шаблон storage_content.html в ответе ' \
            'для htmx запроса'

    @pytest.mark.django_db
    @pytest.mark.parametrize('name', test_args)
    def test_storage_view_create(self, name, auto_login_user):
        client, _ = auto_login_user()
        url = reverse('warehouse:storage-create')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], StorageForm), \
            'Проверьте, что поле `form` содержит объект класса `StorageForm`'

        data = {
            'name': name,
        }
        try:
            response = client.post(url, follow=True, data=data)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'storage' in response.context, \
            'Проверьте, что передали поле `storage` в контекст страницы'
        assert data['name'] == response.context['storage'].name, \
            'Проверьте, что сохраненный экземпляр `storage` содержит' \
            'соответствующее поле `name`'

    @pytest.mark.django_db
    @pytest.mark.parametrize('name', test_args)
    def test_storage_view_update(self, name, auto_login_user, storage_1):
        client, _ = auto_login_user()
        url = reverse('warehouse:storage-update', kwargs={'pk': storage_1.pk})

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], StorageForm), \
            'Проверьте, что поле `form` содержит объект класса `StorageForm`'

        data = {
            'name': name,
        }
        try:
            response = client.post(url, follow=True, data=data)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'storage' in response.context, \
            'Проверьте, что передали поле `storage` в контекст страницы'
        assert data['name'] == response.context['storage'].name, \
            'Проверьте, что измененный экземпляр `storage` содержит' \
            'соответствующее поле `name`'

    @pytest.mark.django_db
    @pytest.mark.parametrize('name', test_args)
    def test_storage_view_delete(self, name, auto_login_user):
        client, user = auto_login_user()
        storage = Storage.objects.create(name=name)
        queryset = Storage.objects.filter(name=name)

        assert queryset.exists(), \
            'Тест работает неправильно, экземпляр `storage` отсутствует в БД'

        url = reverse('warehouse:storage-delete', kwargs={'pk': storage.pk})

        try:
            response = client.delete(url, follow=True)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert not queryset.exists(), \
            'Проверьте, что эксземпляр `storage` удаляется из БД'
