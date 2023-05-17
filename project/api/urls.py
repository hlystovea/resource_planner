from django.urls import include, path
from rest_framework_nested import routers

from .views import (CabinetViewSet, ComponentViewSet, ConnectionViewSet,
                    DefectViewSet, FacilityViewSet, GroupViewSet,
                    HardwareViewSet, PartViewSet)

app_name = 'api'

defect_router = routers.SimpleRouter()
defect_router.register(r'defects', DefectViewSet, basename='defect')

facility_router = routers.SimpleRouter()
facility_router.register(r'facilities', FacilityViewSet, basename='facility')

connection_router = routers.SimpleRouter()
connection_router.register(r'connections', ConnectionViewSet, basename='connection')  # noqa(E501)

group_router = routers.SimpleRouter()
group_router.register(r'groups', GroupViewSet, basename='group')

hardware_router = routers.SimpleRouter()
hardware_router.register(r'hardware', HardwareViewSet, basename='hardware')

cabinet_router = routers.SimpleRouter()
cabinet_router.register(r'cabinets', CabinetViewSet, basename='cabinet')

part_router = routers.SimpleRouter()
part_router.register(r'parts', PartViewSet, basename='part')

component_router = routers.SimpleRouter()
component_router.register(r'components', ComponentViewSet, basename='component')

urlpatterns = [
    path('', include(defect_router.urls)),
    path('', include(facility_router.urls)),
    path('', include(connection_router.urls)),
    path('', include(group_router.urls)),
    path('', include(hardware_router.urls)),
    path('', include(cabinet_router.urls)),
    path('', include(part_router.urls)),
    path('', include(component_router.urls))
]
