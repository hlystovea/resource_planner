from django.urls import path

from warehouse.views import qrcode_view


app_name = 'warehouse'

urlpatterns = [
    path('storage/qr/<int:storage_id>/', qrcode_view, name='storage-qr'),
]
