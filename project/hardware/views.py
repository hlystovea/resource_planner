from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, OuterRef, Prefetch, Subquery, Sum
from django.shortcuts import render
from django.views.generic import (CreateView, DeleteView,
                                  DetailView, ListView, UpdateView)
from django.urls import reverse_lazy

from defects.models import Defect
from hardware.filters import ComponentFilter, ConnectionFilter
from hardware.forms import ComponentForm, ComponentFilterForm
from hardware.models import Component, Connection, Group, Facility
from warehouse.models import ComponentStorage


class ComponentDetail(DetailView):
    model = Component

    def get_queryset(self):
        queryset = super().get_queryset()

        defects = Defect.objects.filter(part__component=OuterRef('pk'))
        count = defects.values('part__component').annotate(count=Count('pk'))
        amount = ComponentStorage.objects.select_related('storage', 'owner')

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComponentFilterForm(self.request.GET or None)
        return context


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
    return render(request, 'hardware/group_select.html', context)


def connection_select_view(request):
    queryset = Connection.objects.all()
    connections = ConnectionFilter(request.GET, queryset=queryset).qs
    context = {'connection_list': connections.select_related('facility')}
    return render(request, 'hardware/connection_select.html', context)


def facility_select_view(request):
    context = {'facility_list': Facility.objects.all()}
    return render(request, 'hardware/facility_select.html', context)
