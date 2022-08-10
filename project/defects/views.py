from django.views.generic import CreateView, DetailView, ListView

from defects.forms import DefectFilterForm
from defects.models import Defect


class DefectList(ListView):
    paginate_by = 20
    model = Defect

    def get_queryset(self):
        queryset = super().get_queryset().select_related('hardware')
        dispatch_object = self.request.GET.get('object')
        connection = self.request.GET.get('connection')
        if dispatch_object and dispatch_object.isdigit():
            queryset = queryset.filter(hardware__facility=dispatch_object)
        if connection and connection.isdigit():
            queryset = queryset.filter(hardware__connection=connection)
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


class DefectCreateView(CreateView):
    model = Defect
    fields = '__all__'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('hardware', 'employee', 'condition')