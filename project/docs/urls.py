from django.urls import path

from docs.views import ProtocolE2CreateView, ProtocolE2DetailView, ProtocolE2ListView


app_name = 'docs'

urlpatterns = [
    path('protocol-e2/<int:pk>', ProtocolE2DetailView.as_view(), name='protocol_e2-detail'),  # noqa(E501)
    path('protocol-e2/create', ProtocolE2CreateView.as_view(), name='protocol_e2-create'),
    path('protocol-e2/', ProtocolE2ListView.as_view(), name='protocol_e2-list'),  # noqa(E501)
]
