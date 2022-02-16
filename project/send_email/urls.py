from django.urls import path

from .views import send, success_view


app_name = 'send_email'

urlpatterns = [
    path('send/', send, name='send'),
    path('success/', success_view, name='success'),
]
