from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  ListView, UpdateView)

from defects.filters import DefectFilter
from defects.forms import DefectForm
from defects.models import Defect


class DefectList(ListView):
    paginate_by = 20
    model = Defect
    queryset = Defect.objects.select_related(
        'part__cabinet__hardware__connection__facility',
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = DefectFilter(self.request.GET, queryset=queryset).qs
        return queryset.order_by('-date')


class DefectDetail(DetailView):
    model = Defect
    queryset = Defect.objects.select_related(
        'employee',
        'condition',
        'part__cabinet__hardware__connection'
    ).prefetch_related(
        'effects',
        'features',
        'technical_reasons',
        'organizational_reasons'
    )


class DefectCreateView(LoginRequiredMixin, CreateView):
    model = Defect
    form_class = DefectForm
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_new'] = True
        return context

    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)


class DefectUpdateView(LoginRequiredMixin, UpdateView):
    model = Defect
    form_class = DefectForm
    login_url = reverse_lazy('login')
    queryset = Defect.objects.select_related(
        'part__cabinet__hardware__connection')


class DefectDeleteView(LoginRequiredMixin, DeleteView):
    model = Defect
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('defects:defect-list')
