from django.urls import path

from warehouse.views import (InstrumentDetail, InstrumentList, MaterialCreate,
                             MaterialDelete, MaterialDetail, MaterialList,
                             MaterialUpdate, MaterialStorageCreate,
                             MaterialStorageDelete, MaterialStorageUpdate,
                             StorageDetail, StorageList, qrcode_view)

app_name = 'warehouse'

urlpatterns = [
    path('instrument/', InstrumentList.as_view(), name='instrument-list'),
    path('instrument/<int:pk>/', InstrumentDetail.as_view(), name='instrument-detail'),  # noqa (E501)
    path('material/', MaterialList.as_view(), name='material-list'),
    path('material/<int:pk>/', MaterialDetail.as_view(), name='material-detail'),  # noqa (E501)
    path('material/<int:pk>/update', MaterialUpdate.as_view(), name='material-update'),  # noqa (E501)
    path('material/<int:pk>/delete', MaterialDelete.as_view(), name='material-delete'),  # noqa (E501)
    path('material/create', MaterialCreate.as_view(), name='material-create'),
    path('storage/', StorageList.as_view(), name='storage-list'),
    path('storage/<int:pk>/', StorageDetail.as_view(), name='storage-detail'),
    path('storage/<int:pk>/qrcode/', qrcode_view, name='storage-qrcode'),
    path('storage/<int:storage_id>/material/<int:material_id>/update', MaterialStorageUpdate.as_view(), name='material-storage-update'),  # noqa (E501)
    path('storage/<int:storage_id>/material/<int:material_id>/delete', MaterialStorageDelete.as_view(), name='material-storage-delete'),  # noqa (E501)
    path('storage/<int:storage_id>/material/create', MaterialStorageCreate.as_view(), name='material-storage-create'),  # noqa (E501)
]
