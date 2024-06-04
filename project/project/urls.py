from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import RedirectView


admin.site.site_title = _('Филиал')
admin.site.site_header = _('Эксплуатация')
admin.site.index_title = _('Администрирование')

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='defects:defect-list'), name='index'),  # noqa (E501)
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls', namespace='api')),
    path('warehouse/', include('warehouse.urls', namespace='warehouse')),
    path('repairs/', include('repairs.urls', namespace='repairs')),
    path('defects/', include('defects.urls', namespace='defects')),
    path('hardware/', include('hardware.urls', namespace='hardware')),
    path('staff/', include('staff.urls', namespace='staff')),
    path('docs/', include('docs.urls', namespace='docs')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # noqa (E501)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # noqa (E501)
