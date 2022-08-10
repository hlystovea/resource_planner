from django.urls import path

from defects.views import DefectCreateView, DefectDetail, DefectList

app_name = 'defects'

urlpatterns = [
    path('', DefectList.as_view(), name='defect-list'),
    path('<int:pk>/', DefectDetail.as_view(), name='defect-detail'),
    path('create/', DefectCreateView.as_view(), name='defect-create')
]