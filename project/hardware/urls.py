from django.urls import path

from hardware import views


app_name = 'hardware'

component_urls = [
    path('components/', views.ComponentList.as_view(), name='component-list'),
    path('components/create/', views.ComponentCreate.as_view(), name='component-create'),  # noqa (E501)
    path('components/<int:pk>/', views.ComponentDetail.as_view(), name='component-detail'),  # noqa (E501)
    path('components/<int:pk>/update/', views.ComponentUpdate.as_view(), name='component-update'),  # noqa (E501)
    path('components/<int:pk>/delete/', views.ComponentDelete.as_view(), name='component-delete'),  # noqa (E501)
]

facility_urls = [
    path('facilities/select/', views.facility_select_view, name='facility-select'),  # noqa (E501)
    path('facilities/<int:pk>/', views.FacilityDetail.as_view(), name='facility-detail'),  # noqa (E501)
    path('facilities/<int:pk>/li/', views.FacilityLiView.as_view(), name='facility-li'),  # noqa (E501)
    path('facilities/<int:pk>/ul/', views.ConnectionUlView.as_view(), name='connection-ul'),  # noqa (E501)
]

connection_urls = [
    path('connections/select/', views.connection_select_view, name='connection-select'),  # noqa (E501)
    path('connections/<int:pk>/', views.ConnectionDetail.as_view(), name='connection-detail'),  # noqa (E501)
    path('connections/<int:pk>/li/', views.ConnectionLiView.as_view(), name='connection-li'),  # noqa (E501)
    path('connections/<int:pk>/ul/', views.HardwareUlView.as_view(), name='hardware-ul'),  # noqa (E501)
]

hardware_urls = [
    path('groups/select/', views.group_select_view, name='group-select'),
    path('hardware/', views.HardwareList.as_view(), name='hardware-list'),
    path('hardware/select/', views.hardware_select_view, name='hardware-select'),  # noqa (E501)
    path('hardware/<int:pk>/', views.HardwareDetail.as_view(), name='hardware-detail'),  # noqa (E501)
    path('hardware/<int:pk>/li/', views.HardwareLiView.as_view(), name='hardware-li'),  # noqa (E501)
    path('hardware/<int:pk>/ul/', views.CabinetUlView.as_view(), name='cabinet-ul'),  # noqa (E501)
]

cabinet_urls = [
    path('cabinets/select/', views.cabinet_select_view, name='cabinet-select'),
    path('cabinets/create/', views.CabinetCreate.as_view(), name='cabinet-create'),  # noqa (E501)
    path('cabinets/<int:pk>/', views.CabinetDetail.as_view(), name='cabinet-detail'),  # noqa (E501)
    path('cabinets/<int:pk>/update/', views.CabinetUpdate.as_view(), name='cabinet-update'),  # noqa (E501)
    path('cabinets/<int:pk>/delete/', views.CabinetDelete.as_view(), name='cabinet-delete'),  # noqa (E501)
    path('cabinets/<int:pk>/inline/', views.CabinetInlineView.as_view(), name='cabinet-inline'),  # noqa (E501)
    path('cabinets/<int:pk>/li/', views.CabinetLiView.as_view(), name='cabinet-li'),  # noqa (E501)
    path('cabinets/<int:pk>/ul/', views.PartUlView.as_view(), name='part-ul'),
]

manufacturer_urls = [
    path('manufacturer/options/', views.manufacturer_options_view, name='manufacturer-options'),  # noqa (E501)
    path('manufacturer/select/', views.manufacturer_select_view, name='manufacturer-select'),  # noqa (E501)
    path('manufacturer/input/', views.manufacturer_input_view, name='manufacturer-input'),  # noqa (E501)
]

part_urls = [
    path('parts/select/', views.part_select_view, name='part-select'),
    path('parts/create/', views.PartCreate.as_view(), name='part-create'),  # noqa (E501)
    path('parts/create/modal/', views.part_create_modal, name='part-create-modal'),  # noqa (E501)
    path('parts/<int:pk>/', views.PartDetail.as_view(), name='part-detail'),
    path('parts/<int:pk>/update/', views.PartUpdate.as_view(), name='part-update'),  # noqa (E501)
    path('parts/<int:pk>/delete/', views.PartDelete.as_view(), name='part-delete'),  # noqa (E501)
    path('parts/<int:pk>/inline/', views.PartInlineView.as_view(), name='part-inline'),  # noqa (E501)
    path('parts/<int:pk>/li/', views.PartLiView.as_view(), name='part-li'),
    path('parts/<int:pk>/ul/', views.PartPartUlView.as_view(), name='part-part-ul'),  # noqa (E501)
]

urlpatterns = (
    component_urls
    + facility_urls
    + connection_urls
    + hardware_urls
    + manufacturer_urls
    + cabinet_urls
    + part_urls
)
