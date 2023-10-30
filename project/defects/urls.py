from django.urls import path

from defects.views import (DefectCreateView, DefectDeleteView,
                           DefectDetail, DefectList, DefectUpdateView,
                           DefectStatisticsView)


app_name = 'defects'

urlpatterns = [
    path('', DefectList.as_view(), name='defect-list'),
    path('<int:pk>', DefectDetail.as_view(), name='defect-detail'),
    path('<int:pk>/update', DefectUpdateView.as_view(), name='defect-update'),
    path('<int:pk>/delete', DefectDeleteView.as_view(), name='defect-delete'),
    path('create', DefectCreateView.as_view(), name='defect-create'),
    path('statistics', DefectStatisticsView.as_view(), name='defect-statistics')  # noqa(E501)
]
