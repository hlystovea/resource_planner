import pytest
from typing import List

from django.urls import reverse
from qr_code.qrcode.utils import QRCodeOptions

from warehouse.models import Storage


@pytest.mark.django_db
def test_storage_view_get_qrcode(client, storage):
    try:
        url = reverse(
            'warehouse:storage-qrcode', kwargs={'pk': storage.id}
        )
        response = client.get(url)
    except Exception as e:
        assert False, f'Страница работает не правильно. Ошибка: {e}'
    assert response.status_code == 200
    assert type(response.context.get('storage')) == Storage, \
        'Проверьте, что передали поле типа Storage в контекст страницы'
    assert type(response.context.get('qr_options')) == QRCodeOptions, \
        'Проверьте, что передали поле типа QRCodeOptions в контекст страницы'


@pytest.mark.django_db
def test_storage_view_get_list(client):
    try:
        url = reverse('warehouse:storage-list')
        response = client.get(url)
    except Exception as e:
        assert False, f'Страница работает не правильно. Ошибка: {e}'
    assert response.status_code == 200
    assert 'storage_list' in response.context, \
        'Проверьте, что передали поле "storage_list" в контекст страницы'


@pytest.mark.django_db
def test_storage_view_get_detail(client, storage):
    try:
        url = reverse(
            'warehouse:storage-detail', kwargs={'pk': storage.id}
        )
        response = client.get(url)
    except Exception as e:
        assert False, f'Страница работает не правильно. Ошибка: {e}'
    assert response.status_code == 200
    assert type(response.context.get('storage')) == Storage, \
        'Проверьте, что передали поле типа Storage в контекст страницы'
