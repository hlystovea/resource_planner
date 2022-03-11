import pytest
from typing import List

from django.urls import reverse
from qr_code.qrcode.utils import QRCodeOptions

from warehouse.models import Instrument, Material, MaterialStorage, Storage


def get_field_context(context, field_type):
    for field in context.keys():
        if field not in ('user', 'request') and type(context[field]) == field_type:
            return context[field]


@pytest.mark.django_db
def test_storage_view_get_qrcode(client, storage_1):
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
def test_storage_view_get_detail(client, storage_1):
    try:
        url = reverse(
            'warehouse:storage-detail', kwargs={'pk': storage_1.id}
        )
        response = client.get(url)
    except Exception as e:
        assert False, f'Страница работает не правильно. Ошибка: {e}'
    assert response.status_code == 200
    storage_from_context = get_field_context(response.context, Storage)
    assert storage_from_context is not None, \
        'Проверьте, что передали поле типа Storage в контекст страницы'


@pytest.mark.django_db
def test_material_view_get_list(client):
    try:
        url = reverse('warehouse:material-list')
        response = client.get(url)
    except Exception as e:
        assert False, f'Страница работает не правильно. Ошибка: {e}'
    assert response.status_code == 200
    assert 'material_list' in response.context, \
        'Проверьте, что передали поле "material_list" в контекст страницы'


@pytest.mark.django_db
def test_material_view_get_detail(client, material, material_in_storage_1, material_in_storage_2):
    try:
        url = reverse(
            'warehouse:material-detail', kwargs={'pk': material.id}
        )
        response = client.get(url)
    except Exception as e:
        assert False, f'Страница работает не правильно. Ошибка: {e}'
    assert response.status_code == 200, \
        'Статус код страницы должен быть 200'

    material_from_context = get_field_context(response.context, Material)

    assert material_from_context is not None, \
        'Проверьте, что передали поле типа Material в контекст страницы'
    assert type(material_from_context.amount.first()) == MaterialStorage, \
        'Проверьте, что вместе с объектом Material передали поле типа MaterialStorage в контекст страницы'
    assert material_from_context.total == material_in_storage_1.amount + material_in_storage_2.amount, \
        'Проверьте, что объект Material содержит поле total с общим количеством материала'


@pytest.mark.django_db
def test_instrument_view_get_list(client):
    try:
        url = reverse('warehouse:instrument-list')
        response = client.get(url)
    except Exception as e:
        assert False, f'Страница работает не правильно. Ошибка: {e}'
    assert response.status_code == 200
    assert 'instrument_list' in response.context, \
        'Проверьте, что передали поле "instrument_list" в контекст страницы'


@pytest.mark.django_db
def test_instrument_view_get_detail(client, instrument):
    try:
        url = reverse(
            'warehouse:instrument-detail', kwargs={'pk': instrument.id}
        )
        response = client.get(url)
    except Exception as e:
        assert False, f'Страница работает не правильно. Ошибка: {e}'
    assert response.status_code == 200
    assert type(response.context.get('instrument')) == Instrument, \
        'Проверьте, что передали поле типа Instrument в контекст страницы'
