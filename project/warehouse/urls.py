from django.urls import path

from warehouse.views import (InstrumentDetail, InstrumentList, MaterialDetail,
                             MaterialList, StorageDetail, StorageList,
                             qrcode_view)

app_name = 'warehouse'

urlpatterns = [
    path('instrument/', InstrumentList.as_view(), name='instrument-list'),
    path('instrument/<int:pk>/', InstrumentDetail.as_view(), name='instrument-detail'),  # noqa (E501)
    path('material/', MaterialList.as_view(), name='material-list'),
    path('material/<int:pk>/', MaterialDetail.as_view(), name='material-detail'),  # noqa (E501)
    path('storage/', StorageList.as_view(), name='storage-list'),
    path('storage/<int:pk>/', StorageDetail.as_view(), name='storage-detail'),
    path('storage/<int:pk>/qrcode/', qrcode_view, name='storage-qrcode'),
]
