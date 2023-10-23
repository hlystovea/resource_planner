from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, OuterRef, Prefetch, Subquery, Sum
from django.views.generic import (CreateView, DeleteView,
                                  DetailView, ListView, UpdateView)
from django.urls import reverse_lazy

from defects.models import Defect
from hardware.filters import ComponentFilter
from hardware.forms import ComponentForm, ComponentFilterForm
from hardware.models import Component
from warehouse.models import ComponentStorage


class ComponentDetail(DetailView):
    model = Component

    def get_queryset(self):
        defects = Defect.objects.filter(part__component=OuterRef('pk'))
        amount = ComponentStorage.objects.select_related('storage', 'owner')
        return Component.objects.annotate(
            defect_count=Count(Subquery(defects.values('pk'))),
            total=Sum('amount__amount')
        ).prefetch_related(
            Prefetch('amount', queryset=amount)
        )


class ComponentList(ListView):
    paginate_by = 20
    model = Component

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = ComponentFilter(self.request.GET, queryset=queryset).qs

        defects = Defect.objects.filter(part__component=OuterRef('pk'))

        queryset = queryset.annotate(
            defect_count=Count(Subquery(defects.values('pk')))
        )
        queryset = queryset.annotate(total=Sum('amount__amount'))

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
