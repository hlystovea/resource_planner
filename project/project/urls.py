from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('warehouse/', include('warehouse.urls', namespace='warehouse')),
    path('repairs/', include('repairs.urls', namespace='repairs')),
]
