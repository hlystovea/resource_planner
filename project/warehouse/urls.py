from django.urls import path

from warehouse import views


app_name = 'warehouse'

urlpatterns = [
    path('instrument/', views.InstrumentList.as_view(), name='instrument-list'),  # noqa (E501)
    path('instrument/<int:pk>/', views.InstrumentDetail.as_view(), name='instrument-detail'),  # noqa (E501)
    path('instrument/<int:pk>/update/', views.InstrumentUpdate.as_view(), name='instrument-update'),  # noqa (E501)
    path('instrument/<int:pk>/delete/', views.InstrumentDelete.as_view(), name='instrument-delete'),  # noqa (E501)
    path('instrument/create/', views.InstrumentCreate.as_view(), name='instrument-create'),  # noqa (E501)
    path('material/', views.MaterialList.as_view(), name='material-list'),
    path('material/create/', views.MaterialCreate.as_view(), name='material-create'),  # noqa (E501)
    path('material/<int:pk>/', views.MaterialDetail.as_view(), name='material-detail'),  # noqa (E501)
    path('material/<int:pk>/update/', views.MaterialUpdate.as_view(), name='material-update'),  # noqa (E501)
    path('material/<int:pk>/delete/', views.MaterialDelete.as_view(), name='material-delete'),  # noqa (E501)
    path('storage/', views.StorageList.as_view(), name='storage-list'),
    path('storage/<int:pk>/', views.StorageDetail.as_view(), name='storage-detail'),  # noqa (E501)
    path('storage/<int:pk>/qrcode/', views.qrcode_view, name='storage-qrcode'),
    path('storage/<int:pk>/update/', views.StorageUpdate.as_view(), name='storage-update'),  # noqa (E501)
    path('storage/<int:pk>/delete/', views.StorageDelete.as_view(), name='storage-delete'),  # noqa (E501)
    path('storage/<int:pk>/add/', views.StorageAdd.as_view(), name='storage-add-storage'),  # noqa (E501)
    path('storage/<int:pk>/li/', views.storage_li_view, name='storage-li'),
    path('storage/create/', views.StorageCreate.as_view(), name='storage-create'),  # noqa (E501)
    path('storage/<int:storage_pk>/material/<int:pk>/', views.MaterialStorageDetail.as_view(), name='material-storage-detail'),  # noqa (E501)
    path('storage/<int:storage_pk>/material/<int:pk>/update/', views.MaterialStorageUpdate.as_view(), name='material-storage-update'),  # noqa (E501)
    path('storage/<int:storage_pk>/material/<int:pk>/delete/', views.MaterialStorageDelete.as_view(), name='material-storage-delete'),  # noqa (E501)
    path('storage/<int:storage_pk>/material/create/', views.MaterialStorageCreate.as_view(), name='material-storage-create'),  # noqa (E501)
    path('storage/<int:storage_pk>/component/<int:pk>/', views.ComponentStorageDetail.as_view(), name='component-storage-detail'),  # noqa (E501)
    path('storage/<int:storage_pk>/component/<int:pk>/update/', views.ComponentStorageUpdate.as_view(), name='component-storage-update'),  # noqa (E501)
    path('storage/<int:storage_pk>/component/<int:pk>/delete/', views.ComponentStorageDelete.as_view(), name='component-storage-delete'),  # noqa (E501)
    path('storage/<int:storage_pk>/component/create/', views.ComponentStorageCreate.as_view(), name='component-storage-create'),  # noqa (E501)
]
