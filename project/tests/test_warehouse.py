import pytest

from django.urls import reverse
from qr_code.qrcode.utils import QRCodeOptions

from warehouse.models import Storage


@pytest.mark.django_db
def test_qr_storage_view_get(client, storage):
    url = reverse('warehouse:storage-qr', kwargs={'storage_id': storage.id})
    response = client.get(url)
    assert response.status_code == 200
    assert type(response.context.get('storage')) == Storage, \
        'Проверьте, что передали поле типа Storage в контекст страницы'
    assert type(response.context.get('qr_options')) == QRCodeOptions, \
        'Проверьте, что передали поле типа QRCodeOptions в контекст страницы'
