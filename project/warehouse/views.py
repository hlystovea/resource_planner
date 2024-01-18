from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Sum, Prefetch
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import (CreateView, DeleteView,
                                  DetailView, ListView, UpdateView)
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from qr_code.qrcode.utils import QRCodeOptions

from core.utils import is_htmx
from warehouse.filters import InstrumentFilter, MaterialFilter
from warehouse.forms import (ComponentStorageForm, InstrumentForm,
                             InstrumentInlineForm, MaterialForm,
                             MaterialInlineForm, MaterialStorageForm,
                             StorageAddForm, StorageForm)
from warehouse.models import (ComponentStorage, Instrument, Material,
                              MaterialStorage, Storage)


def get_url(request, storage: Storage) -> str:
    return request.build_absolute_uri(
        reverse('warehouse:storage-detail', kwargs={'pk': storage.pk})
    )


def qrcode_view(request, pk):
    storage = get_object_or_404(Storage, pk=pk)
    storage_url = get_url(request, storage)
    internal_storage_urls = [
        (s.name, get_url(request, s)) for s in storage.storage.all()
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
        storage = Storage.objects.annotate(materials_count=Count('materials'))
        materials = MaterialStorage.objects.select_related('material')
        components = ComponentStorage.objects.select_related('component')

        return queryset.select_related(
            'parent_storage'
        ).prefetch_related(
            Prefetch('storage', queryset=storage),
            Prefetch('materials', queryset=materials),
            Prefetch('components', queryset=components),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['storage_add_form'] = StorageAddForm()
        context['material_add_form'] = MaterialStorageForm()
        context['component_add_form'] = ComponentStorageForm()
        return context


class StorageList(ListView):
    paginate_by = 20
    model = Storage

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related(
            'parent_storage'
        ).annotate(
            components_count=Count('components')
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


class StorageAdd(StorageCreate):
    form_class = StorageAddForm

    def form_valid(self, form):
        parent_storage = get_object_or_404(Storage, pk=self.kwargs['pk'])
        form.instance.parent_storage = parent_storage
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'warehouse:storage-detail',
            kwargs={'pk': self.kwargs['pk']}
        )


class MaterialDetail(DetailView):
    model = Material

    def get_queryset(self):
        amount = MaterialStorage.objects.select_related('storage', 'owner')
        return Material.objects.annotate(
            total=Sum('amount__amount')
        ).prefetch_related(
            Prefetch('amount', queryset=amount)
        )

    def get_template_names(self):
        if is_htmx(self.request):
            return ['warehouse/material_row.html']
        return ['warehouse/material_detail.html']

class MaterialList(ListView):
    paginate_by = 20
    model = Material

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('amount')
        queryset = MaterialFilter(self.request.GET, queryset=queryset).qs
        return queryset.annotate(total=Sum('amount__amount')).order_by('name')

    def get_template_names(self):
        if is_htmx(self.request):
            return ['warehouse/material_table.html']
        return ['warehouse/material_list.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MaterialInlineForm()
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

    def get_template_names(self):
        if is_htmx(self.request):
            return ['warehouse/material_inline_form.html']
        return ['warehouse/material_form.html']


class MaterialDelete(LoginRequiredMixin, DeleteView):
    model = Material
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('warehouse:material-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()

        if is_htmx(request):
            return HttpResponse()

        return HttpResponseRedirect(success_url)

class InstrumentDetail(DetailView):
    model = Instrument

    def get_queryset(self):
        return super().get_queryset().select_related('owner')

    def get_template_names(self):
        if is_htmx(self.request):
            return ['warehouse/instrument_row.html']
        return ['warehouse/instrument_detail.html']


class InstrumentList(ListView):
    paginate_by = 20
    model = Instrument

    def get_queryset(self):
        queryset = super().get_queryset().select_related('owner')
        queryset = InstrumentFilter(self.request.GET, queryset=queryset).qs
        return queryset.order_by('name')

    def get_template_names(self):
        if is_htmx(self.request):
            return ['warehouse/instrument_table.html']
        return ['warehouse/instrument_list.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InstrumentInlineForm()
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

    def get_template_names(self):
        if is_htmx(self.request):
            return ['warehouse/instrument_inline_form.html']
        return ['warehouse/instrument_form.html']


class InstrumentDelete(LoginRequiredMixin, DeleteView):
    model = Instrument
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('warehouse:instrument-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()

        if is_htmx(request):
            return HttpResponse()

        return HttpResponseRedirect(success_url)


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

        form.instance.owner = self.request.user.dept

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'warehouse:storage-detail',
            kwargs={'pk': self.kwargs['storage_pk']}
        )


class MaterialStorageUpdate(LoginRequiredMixin,
                            UserPassesTestMixin,
                            UpdateView):
    model = MaterialStorage
    form_class = MaterialStorageForm
    login_url = reverse_lazy('login')

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.dept == self.get_object().owner

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


class MaterialStorageDelete(LoginRequiredMixin,
                            UserPassesTestMixin,
                            DeleteView):
    model = MaterialStorage
    login_url = reverse_lazy('login')

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.dept == self.get_object().owner

    def get_success_url(self):
        return reverse(
            'warehouse:storage-detail',
            kwargs={'pk': self.kwargs['storage_pk']}
        )


class ComponentStorageCreate(LoginRequiredMixin, CreateView):
    model = ComponentStorage
    form_class = ComponentStorageForm
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

        form.instance.owner = self.request.user.dept

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'warehouse:storage-detail',
            kwargs={'pk': self.kwargs['storage_pk']}
        )


class ComponentStorageUpdate(LoginRequiredMixin,
                             UserPassesTestMixin,
                             UpdateView):
    model = ComponentStorage
    form_class = ComponentStorageForm
    login_url = reverse_lazy('login')

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.dept == self.get_object().owner

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


class ComponentStorageDelete(LoginRequiredMixin,
                             UserPassesTestMixin,
                             DeleteView):
    model = ComponentStorage
    login_url = reverse_lazy('login')

    def test_func(self):
        user = self.request.user
        return (user.is_superuser
                or user.dept == self.get_object().owner
                or self.get_object().owner is None)

    def get_success_url(self):
        return reverse(
            'warehouse:storage-detail',
            kwargs={'pk': self.kwargs['storage_pk']}
        )
