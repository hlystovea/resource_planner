from django.urls import path

from repairs.views import GeneratePdf


app_name = 'repairs'

urlpatterns = [
    path('<int:repair_id>/pdf', GeneratePdf.as_view(), name='repair-pdf'),
]
