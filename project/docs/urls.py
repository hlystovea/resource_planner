from django.urls import path

from docs import views


app_name = 'docs'

protocol_urls = [
    path('protocols/', views.ProtocolListView.as_view(), name='protocol-list'),
    path('protocols/create/', views.ProtocolCreateView.as_view(), name='protocol-create'),  # noqa (E501)
    path('protocols/<int:pk>/', views.protocol_detail_view, name='protocol-detail'),  # noqa (E501)
    path('protocols/<int:pk>/update/', views.ProtocolUpdateView.as_view(), name='protocol-update'),  # noqa (E501)
    path('protocols/<int:pk>/delete/', views.ProtocolDeleteView.as_view(), name='protocol-delete'),  # noqa (E501)
]

template_urls = [
    path('templates/select/', views.template_select_view, name='template-select'),  # noqa (E501)
]

text_urls = [
    path('texts/create/', views.text_create_view, name='text-create'),
]

integer_urls = [
    path('integers/create/', views.integer_create_view, name='integer-create'),
]

float_urls = [
    path('floats/create/', views.float_create_view, name='float-create'),
]

file_urls = [
    path('images/create/', views.image_create_view, name='image-create'),
    path('images/<int:pk>/delete/', views.image_delete_view, name='image-delete'),  # noqa (E501)
]

urlpatterns = (
    protocol_urls
    + template_urls
    + text_urls
    + integer_urls
    + float_urls
    + file_urls
)
