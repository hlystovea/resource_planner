from django.urls import path

from hardware import views


app_name = 'hardware'

urlpatterns = [
    path('component/', views.ComponentList.as_view(), name='component-list'),
    path('component/<int:pk>/', views.ComponentDetail.as_view(), name='component-detail'),  # noqa (E501)
    path('component/<int:pk>/update/', views.ComponentUpdate.as_view(), name='component-update'),  # noqa (E501)
    path('component/<int:pk>/delete/', views.ComponentDelete.as_view(), name='component-delete'),  # noqa (E501)
    path('component/create/', views.ComponentCreate.as_view(), name='component-create'),  # noqa (E501)
]
