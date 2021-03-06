from django.db.models import Count, Sum, Prefetch
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from qr_code.qrcode.utils import QRCodeOptions

from warehouse.models import Instrument, Material, MaterialStorage, Storage
from warehouse.forms import DeptForm


def get_url(request, storage: Storage) -> str:
    return request.build_absolute_uri(
        reverse('warehouse:storage-detail', kwargs={'pk': storage.id})
    )


def qrcode_view(request, pk):
    storage = get_object_or_404(Storage, pk=pk)
    storage_url = get_url(request, storage)
    internal_storage_urls = [
        (s.name, get_url(request, s))
        for s in storage.storage.all()
        if s.materials.count()
    ]
    qr_options = QRCodeOptions(size='t', border=6, error_correction='L')
    context = {
        'storage': storage,
        'storage_url': storage_url,
        'internal_storage_urls': internal_storage_urls,
        'qr_options': qr_options,
    }
    return render(request, 'warehouse/storage-qrcode.html', context)


class StorageDetail(DetailView):
    model = Storage

    def get_queryset(self):
        queryset = super().get_queryset()
        materials = MaterialStorage.objects.select_related('material')
        storage = Storage.objects.annotate(materials_count=Count('materials'))
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


class MaterialDetail(DetailView):
    model = Material

    def get_queryset(self):
        amount = MaterialStorage.objects.select_related('storage', 'owner')
        return Material.objects.annotate(
            total=Sum('amount__amount')
        ).prefetch_related(
            Prefetch('amount', queryset=amount)
        )


class MaterialList(ListView):
    paginate_by = 20
    model = Material
    template_name = 'warehouse/material_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('amount')
        owner = self.request.GET.get('owner')
        if owner and owner.isdigit():
            queryset = queryset.filter(amount__owner=owner)
        return queryset.annotate(total=Sum('amount__amount')).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DeptForm(self.request.GET or None)
        return context


class InstrumentDetail(DetailView):
    model = Instrument

    def get_queryset(self):
        return super().get_queryset().select_related('owner')


class InstrumentList(ListView):
    paginate_by = 20
    model = Instrument

    def get_queryset(self):
        queryset = super().get_queryset().select_related('owner')
        owner = self.request.GET.get('owner')
        if owner and owner.isdigit():
            queryset = queryset.filter(owner=owner)
        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DeptForm(self.request.GET or None)
        return context
