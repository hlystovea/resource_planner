from django.urls import include, path
from rest_framework_nested import routers

from api.views import DefectViewSet

app_name = 'api'

defect_router = routers.SimpleRouter()
defect_router.register(r'defects', DefectViewSet, basename='defect')

urlpatterns = [
    path('', include(defect_router.urls)),
]
