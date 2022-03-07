from django.db.models import Count, Sum, Prefetch
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import DetailView, ListView
from qr_code.qrcode.utils import QRCodeOptions

from warehouse.models import Instrument, Material, MaterialStorage, Storage


def get_url(request, storage: Storage) -> str:
    return request.build_absolute_uri(
            reverse('warehouse:material-list')
            + '?'
            + urlencode({'storage': f'{storage.id}'})
        )


def qrcode_view(request, pk):
    storage = get_object_or_404(Storage, pk=pk)
    materials_url = None
    if storage.materials.count():
        materials_url = get_url(request, storage)
    internal_storage_urls = [
        [s.name, get_url(request, s)]
        for s in storage.storage.all()
        if s.materials.count()
    ]
    qr_options = QRCodeOptions(size='t', border=6, error_correction='L')
    context = {
        'storage': storage,
        'materials_url': materials_url,
        'internal_storage_urls': internal_storage_urls,
        'qr_options': qr_options,
    }
    return render(request, 'warehouse/storage-qrcode.html', context)


class StorageDetail(DetailView):
    model = Storage

    def get_queryset(self):
        queryset = super().get_queryset()
        materials = MaterialStorage.objects.select_related('material')
        storage = Storage.objects.annotate(
            materials_count=Count('materials')
        ).all()
        return queryset.select_related(
            'parent_storage'
        ).prefetch_related(
            Prefetch('storage', queryset=storage),
            Prefetch('materials', queryset=materials),
        )


class StorageList(ListView):
    paginate_by = 20
    model = Storage

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related(
            'parent_storage'
        ).annotate(
            materials_count=Count('materials')
        ).order_by('name')


class MaterialList(ListView):
    paginate_by = 20
    model = Material
    template_name = 'warehouse/material_list.html'

    def get_queryset(self):
        return Material.objects.annotate(
            total=Sum('amount__amount')
        ).order_by('name')


class MaterialDetail(DetailView):
    model = Material

    def get_queryset(self):
        amount = MaterialStorage.objects.select_related('storage', 'owner')
        return Material.objects.annotate(
            total=Sum('amount__amount')
        ).prefetch_related(
            Prefetch('amount', queryset=amount)
        )


class InstrumentList(ListView):
    paginate_by = 20
    model = Instrument

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'owner'
        ).order_by('name')
        owner = self.request.GET.get('owner')
        if owner and owner.isdigit():
            queryset = queryset.filter(owner=owner)
        return queryset


class InstrumentDetail(DetailView):
    model = Instrument

    def get_queryset(self):
        return super().get_queryset().select_related('owner')
