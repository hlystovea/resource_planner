from django.urls import path

from defects.views import (DefectCreateView, DefectDeleteView,
                           DefectDetailView, DefectListView,
                           DefectUpdateView, DefectStatisticsView,
                           defect_years_view)


app_name = 'defects'

urlpatterns = [
    path('', DefectListView.as_view(), name='defect-list'),
    path('<int:pk>', DefectDetailView.as_view(), name='defect-detail'),
    path('<int:pk>/update', DefectUpdateView.as_view(), name='defect-update'),
    path('<int:pk>/delete', DefectDeleteView.as_view(), name='defect-delete'),
    path('create', DefectCreateView.as_view(), name='defect-create'),
    path('statistics/', DefectStatisticsView.as_view(), name='defect-statistics'),  # noqa(E501)
    path('years/', defect_years_view, name='defect-years'),  # noqa(E501)
]
