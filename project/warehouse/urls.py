from django.urls import path

from warehouse.views import StorageDetailView, StorageListView, qrcode_view

app_name = 'warehouse'

urlpatterns = [
    path('storage/', StorageListView.as_view(), name='storage-list'),
    path('storage/<int:pk>/', StorageDetailView.as_view(), name='storage-detail'),
    path('storage/<int:pk>/qrcode/', qrcode_view, name='storage-qrcode'),
]
