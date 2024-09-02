from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import FieldError
from django.db.models import Count, Prefetch, Sum, Value
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  ListView, TemplateView, UpdateView)
from django.urls import reverse_lazy

from core.utils import is_htmx
from hardware.filters import (CabinetFilter, ComponentFilter, ConnectionFilter,
                              HardwareFilter, PartFilter)
from hardware.forms import (CabinetForm, ComponentForm,
                            ManufacturerForm, PartForm)
from hardware.models import (Cabinet, Component, Connection, Group,
                             Facility, Hardware, Manufacturer, Part)
from warehouse.models import ComponentStorage


class LiViewMixin:
    context_object_name = 'object'
    template_name = 'hardware/includes/menu_li.html'


class UlViewMixin:
    context_object_name = 'object'
    template_name = 'hardware/includes/menu_ul.html'


class ComponentDetail(DetailView):
    model = Component

    def get_queryset(self):
        queryset = super().get_queryset()

        amount = ComponentStorage.objects.select_related('storage__owner')
        parts = Part.objects.select_related('cabinet__hardware__connection__facility')  # noqa (E501)

        queryset = queryset.annotate(
            defect_count=Coalesce(Count('parts__defects', distinct=True), Value(0)),  # noqa (E501)
            in_storage=Coalesce(Sum('amount__amount', distinct=True), Value(0)),  # noqa (E501)
            in_hardware=Coalesce(Count('parts', distinct=True), Value(0))
        )

        return queryset.prefetch_related(
            Prefetch('amount', queryset=amount),
            Prefetch('parts', queryset=parts)
        )


class ComponentList(ListView):
    paginate_by = 50
    model = Component

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = ComponentFilter(self.request.GET, queryset=queryset).qs

        queryset = queryset.annotate(
            defect_count=Coalesce(Count('parts__defects', distinct=True), Value(0)),  # noqa (E501)
            in_storage=Coalesce(Sum('amount__amount', distinct=True), Value(0)),  # noqa (E501)
            in_hardware=Coalesce(Count('parts', distinct=True), Value(0))
        )

        try:
            return queryset.order_by(self.request.GET.get('sort'))
        except FieldError:
            return queryset.order_by('manufacturer', 'name')

    def get_template_names(self):
        if is_htmx(self.request):
            return ['hardware/includes/component_table.html']
        return super().get_template_names()


class ComponentCreate(LoginRequiredMixin, CreateView):
    model = Component
    form_class = ComponentForm
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_new'] = True
        return context


class ComponentUpdate(LoginRequiredMixin, UpdateView):
    model = Component
    form_class = ComponentForm
    login_url = reverse_lazy('login')


class ComponentDelete(LoginRequiredMixin, DeleteView):
    model = Component
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('hardware:component-list')


class FacilityDetail(DetailView):
    queryset = Facility.objects.prefetch_related('connections')

    def get_template_names(self):
        if is_htmx(self.request):
            return ['hardware/includes/facility_content.html']
        return super().get_template_names()


class FacilityLiView(LiViewMixin, DetailView):
    model = Facility


class ConnectionDetail(DetailView):
    queryset = Connection.objects.select_related(
        'facility').prefetch_related('hardware')

    def get_template_names(self):
        if is_htmx(self.request):
            return ['hardware/includes/connection_content.html']
        return super().get_template_names()


class ConnectionLiView(LiViewMixin, DetailView):
    model = Connection


class ConnectionUlView(UlViewMixin, DetailView):
    queryset = Facility.objects.prefetch_related('connections')


class HardwareDetail(DetailView):
    queryset = Hardware.objects.select_related(
        'connection__facility').prefetch_related('cabinets')

    def get_template_names(self):
        if is_htmx(self.request):
            return ['hardware/includes/hardware_content.html']
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cabinet_form'] = CabinetForm()
        return context


class HardwareList(TemplateView):
    template_name = 'hardware/hardware_list.html'

    def get_context_data(self):
        return {'object_list': Facility.objects.order_by('name')}


class HardwareLiView(LiViewMixin, DetailView):
    model = Hardware


class HardwareUlView(UlViewMixin, DetailView):
    queryset = Connection.objects.prefetch_related('hardware')


class CabinetDetail(DetailView):
    model = Cabinet

    def get_queryset(self):
        queryset = super().get_queryset()

        parts = Part.objects.filter(
            part__isnull=True).select_related('component')

        return queryset.select_related(
            'hardware__connection__facility'
        ).prefetch_related(
            Prefetch('parts', queryset=parts),
        )

    def get_template_names(self):
        if is_htmx(self.request):
            return ['hardware/includes/cabinet_content.html']
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['part_form'] = PartForm()
        return context


class CabinetCreate(LoginRequiredMixin, CreateView):
    model = Cabinet
    form_class = CabinetForm
    login_url = reverse_lazy('login')
    success_url = '/hardware/cabinets/{id}/inline/'


class CabinetUpdate(LoginRequiredMixin, UpdateView):
    model = Cabinet
    form_class = CabinetForm
    login_url = reverse_lazy('login')
    success_url = '/hardware/cabinets/{id}/inline/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context


class CabinetDelete(LoginRequiredMixin, DeleteView):
    model = Cabinet
    login_url = reverse_lazy('login')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse()


class CabinetInlineView(DetailView):
    queryset = Cabinet.objects.select_related('manufacturer')
    template_name = 'hardware/includes/cabinet_inline.html'


class CabinetLiView(LiViewMixin, DetailView):
    model = Cabinet


class CabinetUlView(UlViewMixin, DetailView):
    queryset = Hardware.objects.prefetch_related('cabinets')


class PartDetail(DetailView):
    queryset = Part.objects.select_related(
        'cabinet__hardware__connection__facility',
        'component'
    ).prefetch_related(
        'parts__component'
    )

    def get_template_names(self):
        if is_htmx(self.request):
            return ['hardware/includes/part_content.html']
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['part_form'] = PartForm()
        return context


class PartCreate(LoginRequiredMixin, CreateView):
    model = Part
    form_class = PartForm
    login_url = reverse_lazy('login')
    success_url = '/hardware/parts/{id}/inline/'


class PartUpdate(LoginRequiredMixin, UpdateView):
    model = Part
    form_class = PartForm
    login_url = reverse_lazy('login')
    success_url = '/hardware/parts/{id}/inline/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context


class PartDelete(LoginRequiredMixin, DeleteView):
    model = Part
    login_url = reverse_lazy('login')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse()


class PartInlineView(DetailView):
    queryset = Part.objects.select_related('component')
    template_name = 'hardware/includes/part_inline.html'


class PartLiView(LiViewMixin, DetailView):
    model = Part


class PartUlView(UlViewMixin, DetailView):
    queryset = Cabinet.objects.prefetch_related('parts')


class PartPartUlView(UlViewMixin, DetailView):
    queryset = Part.objects.prefetch_related('parts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()
        objects = object.parts.order_by('name')
        context['object_list'] = objects
        return context


def group_select_view(request):
    context = {'group_list': Group.objects.all()}
    return render(request, 'hardware/includes/group_select.html', context)


def facility_select_view(request):
    context = {'facility_list': Facility.objects.all()}
    return render(request, 'hardware/includes/facility_select.html', context)


def connection_select_view(request):
    queryset = Connection.objects.all()
    connections = ConnectionFilter(request.GET, queryset=queryset).qs
    context = {'connection_list': connections.select_related('facility')}
    return render(request, 'hardware/includes/connection_select.html', context)


def hardware_select_view(request):
    queryset = Hardware.objects.all()
    hardware = HardwareFilter(request.GET, queryset=queryset).qs
    context = {'hardware_list': hardware}
    return render(request, 'hardware/includes/hardware_select.html', context)


def cabinet_select_view(request):
    queryset = Cabinet.objects.all()
    cabinets = CabinetFilter(request.GET, queryset=queryset).qs
    context = {'cabinet_list': cabinets}
    return render(request, 'hardware/includes/cabinet_select.html', context)


def part_select_view(request):
    queryset = Part.objects.all()
    parts = PartFilter(request.GET, queryset=queryset).qs
    context = {'part_list': parts.select_related('component')}
    return render(request, 'hardware/includes/part_select.html', context)


def component_select_view(request):
    queryset = Component.objects.all()
    context = {'component_list': queryset.select_related('manufacturer')}
    return render(request, 'hardware/includes/component_select.html', context)


def manufacturer_options_view(request):
    return render(
        request,
        'hardware/includes/manufacturer_options.html',
        context={
            'manufacturer_list': Manufacturer.objects.all(),
        }
    )


def manufacturer_select_view(request):
    return render(
        request,
        'hardware/includes/manufacturer_select.html',
        context={
            'selected_manufacturer': None,
            'manufacturer_list': Manufacturer.objects.all(),
        }
    )


@login_required
def manufacturer_input_view(request):
    form = ManufacturerForm(request.POST or None)
    if form.is_valid():
        manufacturer = form.save()
        return render(
            request,
            'hardware/includes/manufacturer_select.html',
            context={
                'selected_manufacturer': manufacturer.pk,
                'manufacturer_list': Manufacturer.objects.all(),
            }
        )
    return render(
        request,
        'hardware/includes/manufacturer_input.html',
        context={
            'form': form,
        }
    )


@login_required
def part_create_modal(request):
    form = PartForm(request.POST or None)
    context = {}

    if form.is_valid():
        part = form.save()
        return render(
            request,
            'hardware/includes/part_create_success_modal.html',
            context={'part': part}
        )

    if request.GET.get('cabinet'):
        cabinet = get_object_or_404(Cabinet, pk=request.GET.get('cabinet'))
        context |= {'cabinet': cabinet}

    if request.GET.get('part'):
        part = get_object_or_404(Part, pk=request.GET.get('part'))
        context |= {'parent_part': part}

    return render(
        request,
        'hardware/includes/part_form_modal.html',
        context | {'form': form}
    )


@login_required
def component_create_modal(request):
    form = ComponentForm(request.POST or None)
    context = {}

    if form.is_valid():
        component = form.save()
        return render(
            request,
            'hardware/includes/component_create_success_modal.html',
            context={'component': component}
        )

    return render(
        request,
        'hardware/includes/component_form_modal.html',
        context | {'form': form}
    )
