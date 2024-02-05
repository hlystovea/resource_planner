from django.urls import path

from hardware import views


app_name = 'hardware'

urlpatterns = [
    path('component/', views.ComponentList.as_view(), name='component-list'),
    path('component/<int:pk>/', views.ComponentDetail.as_view(), name='component-detail'),  # noqa (E501)
    path('component/<int:pk>/update/', views.ComponentUpdate.as_view(), name='component-update'),  # noqa (E501)
    path('component/<int:pk>/delete/', views.ComponentDelete.as_view(), name='component-delete'),  # noqa (E501)
    path('component/create/', views.ComponentCreate.as_view(), name='component-create'),  # noqa (E501)
    path('groups/select/', views.group_select_view, name='group-select'),
    path('facilities/select/', views.facility_select_view, name='facility-select'),  # noqa (E501)
    path('connections/select/', views.connection_select_view, name='connection-select'),  # noqa (E501)
    path('hardware/', views.HardwareList.as_view(), name='hardware-list'),
    path('hardware/select/', views.hardware_select_view, name='hardware-select'),  # noqa (E501)
    path('cabinets/select/', views.cabinet_select_view, name='cabinet-select'),
    path('parts/select/', views.part_select_view, name='part-select'),
    path('manufacturer/options/', views.manufacturer_options_view, name='manufacturer-options'),  # noqa (E501)
    path('manufacturer/select/', views.manufacturer_select_view, name='manufacturer-select'),  # noqa (E501)
    path('manufacturer/input/', views.manufacturer_input_view, name='manufacturer-input'),  # noqa (E501)
]
