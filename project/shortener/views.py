from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404


from .models import Shortener


def redirect_url_view(request, shortened_part):
    shortener = get_object_or_404(Shortener, short_url=shortened_part)
    return HttpResponseRedirect(shortener.long_url)
