from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum, Prefetch
from django.views.generic import (CreateView, DeleteView,
                                  DetailView, ListView, UpdateView)
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from qr_code.qrcode.utils import QRCodeOptions

from warehouse.models import Instrument, Material, MaterialStorage, Storage
from warehouse.forms import (DeptForm, InstrumentForm, MaterialForm,
                             MaterialStorageForm, StorageForm)


def get_url(request, storage: Storage) -> str:
    return request.build_absolute_uri(
        reverse('warehouse:storage-detail', kwargs={'pk': storage.pk})
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MaterialStorageForm()
        return context


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


class StorageCreate(LoginRequiredMixin, CreateView):
    model = Storage
    form_class = StorageForm
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_new'] = True
        return context


class StorageUpdate(LoginRequiredMixin, UpdateView):
    model = Storage
    form_class = StorageForm
    login_url = reverse_lazy('login')


class StorageDelete(LoginRequiredMixin, DeleteView):
    model = Storage
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('warehouse:storage-list')


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


class MaterialCreate(LoginRequiredMixin, CreateView):
    model = Material
    form_class = MaterialForm
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_new'] = True
        return context


class MaterialUpdate(LoginRequiredMixin, UpdateView):
    model = Material
    form_class = MaterialForm
    login_url = reverse_lazy('login')


class MaterialDelete(LoginRequiredMixin, DeleteView):
    model = Material
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('warehouse:material-list')


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


class InstrumentCreate(LoginRequiredMixin, CreateView):
    model = Instrument
    form_class = InstrumentForm
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_new'] = True
        return context

    def form_valid(self, form):
        if not hasattr(form.instance, 'owner'):
            form.instance.owner = self.request.user.dept

        return super().form_valid(form)


class InstrumentUpdate(LoginRequiredMixin, UpdateView):
    model = Instrument
    form_class = InstrumentForm
    login_url = reverse_lazy('login')


class InstrumentDelete(LoginRequiredMixin, DeleteView):
    model = Instrument
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('warehouse:instrument-list')


class MaterialStorageCreate(LoginRequiredMixin, CreateView):
    model = MaterialStorage
    form_class = MaterialStorageForm
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        storage = get_object_or_404(Storage, pk=self.kwargs['storage_pk'])
        context['storage'] = storage
        context['is_new'] = True
        return context

    def form_valid(self, form):
        if not hasattr(form.instance, 'storage'):
            storage = get_object_or_404(Storage, pk=self.kwargs['storage_pk'])
            form.instance.storage = storage

        if not hasattr(form.instance, 'owner'):
            form.instance.owner = self.request.user.dept

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'warehouse:storage-detail',
            kwargs={'pk': self.kwargs['storage_pk']}
        )


class MaterialStorageUpdate(LoginRequiredMixin, UpdateView):
    model = MaterialStorage
    form_class = MaterialStorageForm
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        storage = get_object_or_404(Storage, pk=self.kwargs['storage_pk'])
        context['storage'] = storage
        return context

    def get_success_url(self):
        return reverse(
            'warehouse:storage-detail',
            kwargs={'pk': self.kwargs['storage_pk']}
        )


class MaterialStorageDelete(LoginRequiredMixin, DeleteView):
    model = MaterialStorage
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse(
            'warehouse:storage-detail',
            kwargs={'pk': self.kwargs['storage_pk']}
        )
