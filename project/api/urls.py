from django.urls import include, path
from rest_framework_nested import routers

from .views import (CabinetViewSet, ComponentViewSet, ConnectionViewSet, 
                    FacilityViewSet, GroupViewSet, HardwareViewSet)

app_name = 'api'

facility_router = routers.SimpleRouter()
facility_router.register(r'facilities', FacilityViewSet, basename='facility')

connection_router = routers.SimpleRouter()
connection_router.register(r'connections', ConnectionViewSet, basename='connection')

group_router = routers.SimpleRouter()
group_router.register(r'groups', GroupViewSet, basename='group')

hardware_router = routers.SimpleRouter()
hardware_router.register(r'hardware', HardwareViewSet, basename='hardware')

cabinet_router = routers.SimpleRouter()
cabinet_router.register(r'cabinets', CabinetViewSet, basename='cabinet')

component_router = routers.SimpleRouter()
component_router.register(r'components', ComponentViewSet, basename='component')

urlpatterns = [
    path('', include(facility_router.urls)),
    path('', include(connection_router.urls)),
    path('', include(group_router.urls)),
    path('', include(hardware_router.urls)),
    path('', include(cabinet_router.urls)),
    path('', include(component_router.urls))
]
