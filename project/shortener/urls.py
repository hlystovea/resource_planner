from django.urls import path

from .views import redirect_url_view

appname = 'shortener'

urlpatterns = [
    path('links/<str:shortened_part>', redirect_url_view, name='redirect')
]
