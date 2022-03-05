from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import IndexPageView


admin.site.site_title = 'Филиал'
admin.site.site_header = 'Сервис'
admin.site.index_title = 'Управление'

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('warehouse/', include('warehouse.urls', namespace='warehouse')),
    path('repairs/', include('repairs.urls', namespace='repairs')),
    path('emails/', include('send_email.urls', namespace='send_email')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
