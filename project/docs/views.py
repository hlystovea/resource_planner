from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import ExtractYear
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from core.utils import is_htmx
from docs.filters import ProtocolE2Filter
from docs.forms import ProtocolE2Form
from docs.models import ProtocolE2


class ProtocolE2ListView(ListView):
    model = ProtocolE2

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = ProtocolE2Filter(self.request.GET, queryset=queryset).qs
        queryset = queryset.select_related('connection')
        return queryset.order_by('-date')

    def get_template_names(self):
        if is_htmx(self.request):
            return ['docs/includes/protocole2_table.html']
        return ['docs/protocole2_list.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year_list'] = ProtocolE2.objects.dates(
            'date',
            'year'
        ).values_list(
            ExtractYear('date'),
            flat=True
        )
        return context


class ProtocolE2DetailView(DetailView):
    model = ProtocolE2


class ProtocolE2CreateView(LoginRequiredMixin, CreateView):
    model = ProtocolE2
    form_class = ProtocolE2Form
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('docs:protocol_e2-list')
