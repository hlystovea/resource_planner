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
    path('texts/create/', views.text_update_or_create_view, name='text-create'),  # noqa (E501)
    path('texts/<int:pk>/update/', views.text_update_or_create_view, name='text-update'),  # noqa (E501)
]

char_urls = [
    path('chars/create/', views.char_update_or_create_view, name='char-create'),  # noqa (E501)
    path('chars/<int:pk>/update/', views.char_update_or_create_view, name='char-update'),  # noqa (E501)
]

integer_urls = [
    path('integers/create/', views.integer_update_or_create_view, name='integer-create'),  # noqa (E501)
    path('integers/<int:pk>/update/', views.integer_update_or_create_view, name='integer-update'),  # noqa (E501)
]

float_urls = [
    path('floats/create/', views.float_update_or_create_view, name='float-create'),  # noqa (E501)
    path('floats/<int:pk>/update/', views.float_update_or_create_view, name='float-update'),  # noqa (E501)
]

file_urls = [
    path('images/create/', views.image_create_view, name='image-create'),
    path('images/<int:pk>/delete/', views.image_delete_view, name='image-delete'),  # noqa (E501)
]

urlpatterns = (
    protocol_urls
    + template_urls
    + text_urls
    + char_urls
    + integer_urls
    + float_urls
    + file_urls
)
