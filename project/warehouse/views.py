from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.http import urlencode
from qr_code.qrcode.utils import QRCodeOptions

from warehouse.models import Storage


def get_url(request, storage: Storage) -> str:
    return request.build_absolute_uri(
            reverse('admin:warehouse_materialstorage_changelist')
            + '?'
            + urlencode({'storage__id': f'{storage.id}'})
        )


def qrcode_view(request, storage_id):
    storage = get_object_or_404(Storage.objects.filter(id=storage_id))
    if storage.materials.count():
        materials_url = get_url(request, storage)
    internal_storage_urls = [
        [s.name, get_url(request, s)] for s in storage.storage.all() if s.materials.count()
    ]
    qr_options = QRCodeOptions(size='t', border=6, error_correction='L')
    context = {
        'storage': storage,
        'materials_url': materials_url or None,
        'internal_storage_urls': internal_storage_urls,
        'qr_options': qr_options,
    }
    return render(request, 'warehouse/qrcode.html', context)
