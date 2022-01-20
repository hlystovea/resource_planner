from django.contrib import admin
from django.urls import include, path


admin.site.site_title = 'Филиал'
admin.site.site_header = 'Сервис'
admin.site.index_title = 'Управление'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('warehouse/', include('warehouse.urls', namespace='warehouse')),
    path('repairs/', include('repairs.urls', namespace='repairs')),
]
