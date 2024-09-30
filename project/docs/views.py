from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import ExtractYear
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.template import Template as TemplateClass
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView,
                                  DetailView, ListView, UpdateView)

from core.utils import is_htmx
from docs.filters import ProtocolE2Filter, ProtocolFilter
from docs.forms import (ImageForm, ProtocolE2Form,
                        ProtocolForm, TextForm)
from docs.models import Protocol, ProtocolE2, Template, File


class ProtocolE2ListView(ListView):
    model = ProtocolE2

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = ProtocolE2Filter(self.request.GET, queryset=queryset).qs
        queryset = queryset.select_related(
            'connection', 'supervisor'
        ).prefetch_related(
            'signers'
        )
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
    queryset = ProtocolE2.objects.select_related(
        'connection', 'supervisor__dept__service'
    ).prefetch_related(
        'signers__dept__service'
    )


class ProtocolE2CreateView(LoginRequiredMixin, CreateView):
    model = ProtocolE2
    form_class = ProtocolE2Form
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('docs:protocol_e2-list')


class ProtocolE2UpdateView(LoginRequiredMixin, UpdateView):
    model = ProtocolE2
    form_class = ProtocolE2Form
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('docs:protocol_e2-list')


class ProtocolE2DeleteView(LoginRequiredMixin, DeleteView):
    model = ProtocolE2
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('docs:protocol_e2-list')


class ProtocolListView(ListView):
    model = Protocol
    login_url = reverse_lazy('login')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = ProtocolFilter(self.request.GET, queryset=queryset).qs
        queryset = queryset.select_related(
            'connection', 'supervisor', 'template'
        ).prefetch_related(
            'signers'
        )
        return queryset.order_by('-date')

    def get_template_names(self):
        if is_htmx(self.request):
            return ['docs/includes/protocol_table.html']
        return ['docs/protocol_list.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year_list'] = Protocol.objects.dates(
            'date',
            'year'
        ).values_list(
            ExtractYear('date'),
            flat=True
        )
        return context


class ProtocolCreateView(LoginRequiredMixin, CreateView):
    model = Protocol
    form_class = ProtocolForm
    login_url = reverse_lazy('login')


class ProtocolUpdateView(LoginRequiredMixin, UpdateView):
    model = Protocol
    form_class = ProtocolForm
    login_url = reverse_lazy('login')


class ProtocolDeleteView(LoginRequiredMixin, DeleteView):
    model = Protocol
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('docs:protocol-list')


class ImageDeleteView(LoginRequiredMixin, DeleteView):
    model = File
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('docs:image-create')


def protocol_detail_view(request, pk):
    queryset = Protocol.objects.select_related(
        'connection', 'template', 'supervisor__dept__service'
    ).prefetch_related(
        'signers__dept__service'
    )

    protocol = get_object_or_404(queryset, pk=pk)

    with open(protocol.template.file.path, 'r') as file:
        template_content = file.read()

    template = TemplateClass(template_content)

    context = RequestContext(request)
    context['protocol'] = protocol

    return HttpResponse(template.render(context))


@login_required
def text_create_view(request):
    template = 'docs/includes/text_element.html'
    form = TextForm(request.POST or None)

    if form.is_valid():
        text = form.save()
        return render(request, template, {'text': text})

    return render(request, template, {'form': form})


@login_required
def image_create_view(request):
    template = 'docs/includes/image_element.html'

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.save()
            return render(request, template, {'image': file})

    else:
        form = ImageForm()

    return render(request, template, {'form': form})


@login_required
def image_delete_view(request, pk):
    image = get_object_or_404(File, pk=pk)

    if request.method == 'POST' or 'DELETE':
        context = {
            'form': ImageForm(),
            'protocol_pk': image.protocol.pk,
            'slug': image.slug,
        }
        image.delete()

        return render(request, 'docs/includes/image_element.html', context)

    return HttpResponseNotAllowed(('POST', 'DELETE'))


def template_select_view(request):
    context = {'template_list': Template.objects.all()}
    return render(request, 'docs/includes/template_select.html', context)
