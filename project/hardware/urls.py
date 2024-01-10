from django.urls import path

from hardware import views


app_name = 'hardware'

urlpatterns = [
    path('component/', views.ComponentList.as_view(), name='component-list'),
    path('component/<int:pk>/', views.ComponentDetail.as_view(), name='component-detail'),  # noqa (E501)
    path('component/<int:pk>/update/', views.ComponentUpdate.as_view(), name='component-update'),  # noqa (E501)
    path('component/<int:pk>/delete/', views.ComponentDelete.as_view(), name='component-delete'),  # noqa (E501)
    path('component/create/', views.ComponentCreate.as_view(), name='component-create'),
    path('groups/select/', views.group_select_view, name='group-select'),
    path('connections/select/', views.connection_select_view, name='connection-select'),
    path('facilities/select/', views.facility_select_view, name='facility-select'),
]
