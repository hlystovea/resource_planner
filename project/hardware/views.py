from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, OuterRef, Prefetch, Subquery, Sum
from django.shortcuts import render
from django.views.generic import (CreateView, DeleteView,
                                  DetailView, ListView, UpdateView)
from django.urls import reverse_lazy

from core.utils import is_htmx
from defects.models import Defect
from hardware.filters import (CabinetFilter, ComponentFilter, ConnectionFilter,
                              HardwareFilter, PartFilter)
from hardware.forms import ComponentForm, ManufacturerForm
from hardware.models import (Cabinet, Component, Connection, Group,
                             Facility, Hardware, Manufacturer, Part)
from warehouse.models import ComponentStorage


class ComponentDetail(DetailView):
    model = Component

    def get_queryset(self):
        queryset = super().get_queryset()

        defects = Defect.objects.filter(part__component=OuterRef('pk'))
        count = defects.values('part__component').annotate(count=Count('pk'))
        amount = ComponentStorage.objects.select_related('storage__owner')

        queryset = queryset.annotate(
            defect_count=Subquery(count.values('count')),
            total=Sum('amount__amount')
        )
        return queryset.prefetch_related(Prefetch('amount', queryset=amount))


class ComponentList(ListView):
    paginate_by = 20
    model = Component

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = ComponentFilter(self.request.GET, queryset=queryset).qs

        defects = Defect.objects.filter(part__component=OuterRef('pk'))
        count = defects.values('part__component').annotate(count=Count('pk'))

        queryset = queryset.annotate(
            defect_count=Subquery(count.values('count')),
            total=Sum('amount__amount')
        )
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


def manufacturer_select_view(request):
    context = {'manufacturer_list': Manufacturer.objects.all()}
    return render(request, 'hardware/includes/manufacturer_options.html', context)


@login_required
def manufacturer_input_view(request):
    form = ManufacturerForm(request.POST or None)
    if form.is_valid():
        manufacturer = form.save()
        return render(
            request,
            'hardware/includes/manufacturer_select.html',
            context={
                'selected_manufacturer': manufacturer,
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
