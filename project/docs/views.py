from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import ExtractYear
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.template import Template as TemplateClass
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView,
                                  DetailView, ListView, UpdateView)

from core.utils import is_htmx
from docs.filters import ProtocolFilter
from docs.forms import (CharForm, FloatForm, ImageForm,
                        IntegerForm, ProtocolForm, TextForm)
from docs.models import Integer, File, Float, Protocol, Template, Text


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


class TextDetailView(DetailView):
    model = Text
    template_name = 'docs/text_element.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse_lazy(
            'docs:text-update',
            kwargs={'pk': self.kwargs['pk']}
        )
        return context


class TextCreateView(LoginRequiredMixin, CreateView):
    model = Text
    form_class = TextForm
    login_url = reverse_lazy('login')
    success_url = '/docs/texts/{id}/'
    template_name = 'docs/text_element.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse_lazy('docs:text-create')
        return context


class TextUpdateView(LoginRequiredMixin, UpdateView):
    model = Text
    form_class = TextForm
    login_url = reverse_lazy('login')
    success_url = '/docs/texts/{id}/'
    template_name = 'docs/text_element.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse_lazy(
            'docs:text-update',
            kwargs={'pk': self.kwargs['pk']}
        )
        return context


class CharDetailView(DetailView):
    model = Text
    template_name = 'docs/base_element.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse_lazy(
            'docs:char-update',
            kwargs={'pk': self.kwargs['pk']}
        )
        return context


class CharCreateView(LoginRequiredMixin, CreateView):
    model = Text
    form_class = CharForm
    login_url = reverse_lazy('login')
    success_url = '/docs/chars/{id}/'
    template_name = 'docs/base_element.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse_lazy('docs:char-create')
        return context


class CharUpdateView(LoginRequiredMixin, UpdateView):
    model = Text
    form_class = CharForm
    login_url = reverse_lazy('login')
    success_url = '/docs/chars/{id}/'
    template_name = 'docs/base_element.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse_lazy(
            'docs:char-update',
            kwargs={'pk': self.kwargs['pk']}
        )
        return context


class IntegerDetailView(DetailView):
    model = Integer
    template_name = 'docs/base_element.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse_lazy(
            'docs:integer-update',
            kwargs={'pk': self.kwargs['pk']}
        )
        return context


class IntegerCreateView(LoginRequiredMixin, CreateView):
    model = Integer
    form_class = IntegerForm
    login_url = reverse_lazy('login')
    success_url = '/docs/integers/{id}/'
    template_name = 'docs/base_element.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse_lazy('docs:integer-create')
        return context


class IntegerUpdateView(LoginRequiredMixin, UpdateView):
    model = Integer
    form_class = IntegerForm
    login_url = reverse_lazy('login')
    success_url = '/docs/integers/{id}/'
    template_name = 'docs/base_element.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse_lazy(
            'docs:integer-update',
            kwargs={'pk': self.kwargs['pk']}
        )
        return context


class FloatDetailView(DetailView):
    model = Float
    template_name = 'docs/base_element.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse_lazy(
            'docs:float-update',
            kwargs={'pk': self.kwargs['pk']}
        )
        return context


class FloatCreateView(LoginRequiredMixin, CreateView):
    model = Float
    form_class = FloatForm
    login_url = reverse_lazy('login')
    success_url = '/docs/floats/{id}/'
    template_name = 'docs/base_element.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse_lazy('docs:float-create')
        return context


class FloatUpdateView(LoginRequiredMixin, UpdateView):
    model = Float
    form_class = FloatForm
    login_url = reverse_lazy('login')
    success_url = '/docs/floats/{id}/'
    template_name = 'docs/base_element.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse_lazy(
            'docs:float-update',
            kwargs={'pk': self.kwargs['pk']}
        )
        return context


class ImageDetailView(DetailView):
    model = File
    template_name = 'docs/image_element.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse_lazy(
            'docs:image-delete',
            kwargs={'pk': self.kwargs['pk']}
        )
        return context


class ImageCreateView(LoginRequiredMixin, CreateView):
    model = File
    form_class = ImageForm
    login_url = reverse_lazy('login')
    success_url = '/docs/images/{id}/'
    template_name = 'docs/image_element.html'


class ImageDeleteView(LoginRequiredMixin, DeleteView):
    model = File
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        context = {
            'form': ImageForm(),
            'protocol_pk': self.object.protocol.pk,
            'slug': self.object.slug,
        }
        self.object.delete()
        return render(self.request, 'docs/image_element.html', context)


def template_select_view(request):
    context = {'template_list': Template.objects.all()}
    return render(request, 'docs/includes/template_select.html', context)
