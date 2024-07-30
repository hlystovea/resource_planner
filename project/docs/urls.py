from django.urls import path

from docs.views import (ProtocolE2CreateView, ProtocolE2DeleteView,
                        ProtocolE2DetailView, ProtocolE2ListView,
                        ProtocolE2UpdateView)


app_name = 'docs'

urlpatterns = [
    path('protocol-e2/<int:pk>', ProtocolE2DetailView.as_view(), name='protocol_e2-detail'),  # noqa(E501)
    path('protocol-e2/create', ProtocolE2CreateView.as_view(), name='protocol_e2-create'),  # noqa(E501)
    path('protocol-e2/<int:pk>/update', ProtocolE2UpdateView.as_view(), name='protocol_e2-update'),  # noqa(E501)
    path('protocol-e2/<int:pk>/delete', ProtocolE2DeleteView.as_view(), name='protocol_e2-delete'),  # noqa(E501)
    path('protocol-e2/', ProtocolE2ListView.as_view(), name='protocol_e2-list'),  # noqa(E501)
]
