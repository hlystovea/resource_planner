from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import DetailView, ListView
from qr_code.qrcode.utils import QRCodeOptions

from warehouse.models import Storage


def get_url(request, storage: Storage) -> str:
    return request.build_absolute_uri(
            reverse('admin:warehouse_materialstorage_changelist')
            + '?'
            + urlencode({'storage__id': f'{storage.id}'})
        )


def qrcode_view(request, pk):
    storage = get_object_or_404(Storage, pk=pk)
    materials_url = None
    if storage.materials.count():
        materials_url = get_url(request, storage)
    internal_storage_urls = [
        [s.name, get_url(request, s)] for s in storage.storage.all() if s.materials.count()  # noqa (E501)
    ]
    qr_options = QRCodeOptions(size='t', border=6, error_correction='L')
    context = {
        'storage': storage,
        'materials_url': materials_url,
        'internal_storage_urls': internal_storage_urls,
        'qr_options': qr_options,
    }
    return render(request, 'warehouse/storage-qrcode.html', context)


def storage_view_list(request):
    storages = get_list_or_404(
        Storage.objects.all()
    )
    context = {
        'storages': storages,
    }
    return render(request, 'warehouse/storage_list.html', context)


def storage_view_detail(request, storage_id):
    storage = get_object_or_404(Storage, id=storage_id)
    context = {
        'storage': storage,
    }
    return render(request, 'warehouse/storage_list.html', context)


class StorageDetailView(DetailView):
    model = Storage


class StorageListView(ListView):
    model = Storage
