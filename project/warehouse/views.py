from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import DetailView, ListView
from qr_code.qrcode.utils import QRCodeOptions

from warehouse.models import Instrument, Material, Storage


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['storage_list'] = self.get_object().storage.annotate(
            materials_count=Count('materials')).all()
        context['material_list'] = self.get_object().materials.all()
        return context


class StorageList(ListView):
    paginate_by = 20
    model = Storage

    def get_queryset(self):
        queryset = Storage.objects.annotate(
            materials_count=Count('materials')
        ).order_by(
            'name'
        )
        parent_storage = self.request.GET.get('parent_storage')
        if parent_storage and parent_storage.isdigit():
            queryset = queryset.filter(parent_storage=parent_storage)
        return queryset


class MaterialList(ListView):
    paginate_by = 20
    model = Material
    template_name = 'warehouse/material_list.html'

    def get_queryset(self):
        queryset = Material.objects.annotate(
            total=Sum('amount__amount')).all()
        storage = self.request.GET.get('storage')
        if storage and storage.isdigit():
            queryset = queryset.filter(amount__storage=storage)
        return queryset


class MaterialDetail(DetailView):
    model = Material

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['storage_list'] = self.get_object().amount.all()
        return context


class InstrumentList(ListView):
    paginate_by = 20
    model = Instrument

    def get_queryset(self):
        queryset = Instrument.objects.all()
        owner = self.request.GET.get('owner')
        if owner and owner.isdigit():
            queryset = queryset.filter(owner=owner)
        return queryset


class InstrumentDetail(DetailView):
    model = Instrument
