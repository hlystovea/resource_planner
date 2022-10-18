from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from defects.forms import DefectFilterForm, DefectForm
from defects.models import Defect


class DefectList(ListView):
    paginate_by = 20
    model = Defect

    def get_queryset(self):
        queryset = super().get_queryset().select_related('hardware')

        facility = self.request.GET.get('facility')
        connection = self.request.GET.get('connection')
        hardware = self.request.GET.get('hardware')
        cabinet = self.request.GET.get('cabinet')

        if facility and facility.isdigit():
            queryset = queryset.filter(hardware__connection__facility=facility)
        if connection and connection.isdigit():
            queryset = queryset.filter(hardware__connection=connection)
        if hardware and hardware.isdigit():
            queryset = queryset.filter(hardware=hardware)
        if cabinet and cabinet.isdigit():
            queryset = queryset.filter(cabinet=cabinet)

        return queryset.order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DefectFilterForm(self.request.GET or None)
        return context


class DefectDetail(DetailView):
    model = Defect

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('hardware', 'employee', 'condition')


class DefectCreateView(LoginRequiredMixin, CreateView):
    model = Defect
    form_class = DefectForm
    login_url = '/auth/login/'

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
    login_url = '/auth/login/'


class DefectDeleteView(DeleteView):
    model = Defect
    success_url = reverse_lazy('defects:defect-list')
