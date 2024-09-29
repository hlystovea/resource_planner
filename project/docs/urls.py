from django.urls import path

from docs import views


app_name = 'docs'

protocol_urls = [
    path('protocols/', views.ProtocolListView.as_view(), name='protocol-list'),
    path('protocols/create/', views.ProtocolCreateView.as_view(), name='protocol-create'),  # noqa (E501)
    path('protocols/<int:pk>/', views.protocol_detail_view, name='protocol-detail'),  # noqa (E501)
    path('protocols/<int:pk>/update/', views.ProtocolUpdateView.as_view(), name='protocol-update'),  # noqa (E501)
    path('protocols/<int:pk>/delete/', views.ProtocolDeleteView.as_view(), name='protocol-delete'),  # noqa (E501)
    path('protocol-e2/', views.ProtocolE2ListView.as_view(), name='protocol_e2-list'),  # noqa (E501)
    path('protocol-e2/create/', views.ProtocolE2CreateView.as_view(), name='protocol_e2-create'),  # noqa (E501)
    path('protocol-e2/<int:pk>/', views.ProtocolE2DetailView.as_view(), name='protocol_e2-detail'),  # noqa (E501)
    path('protocol-e2/<int:pk>/update/', views.ProtocolE2UpdateView.as_view(), name='protocol_e2-update'),  # noqa (E501)
    path('protocol-e2/<int:pk>/delete/', views.ProtocolE2DeleteView.as_view(), name='protocol_e2-delete'),  # noqa (E501)
]

template_urls = [
    path('templates/select/', views.template_select_view, name='template-select'),  # noqa (E501)
]

text_urls = [
    path('texts/create/', views.text_create_view, name='text-create'),
]

file_urls = [
    path('images/create/', views.image_create_view, name='image-create'),
]

urlpatterns = protocol_urls + template_urls + text_urls + file_urls
