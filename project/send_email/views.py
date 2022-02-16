from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import ContactForm


def send(request):
    if request.method == 'GET':
        form = ContactForm()
    elif request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(f'{subject} от {from_email}', message,
                          settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Ошибка в теме письма.')
            return redirect('send_email:success')
    else:
        return HttpResponse('Неверный запрос.')
    return render(request, "send_email/email.html", {'form': form})


def success_view(request):
    return HttpResponse('Приняли! Спасибо за вашу заявку.')
