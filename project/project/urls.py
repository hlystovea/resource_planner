from constance import config
from django.conf import settings
from django.conf.urls import handler400, handler403, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import RedirectView


handler400 = 'core.views.error_400_handler'  # noqa (F811)
handler403 = 'core.views.error_403_handler'  # noqa (F811)
handler404 = 'core.views.error_404_handler'  # noqa (F811)
handler500 = 'core.views.error_500_handler'  # noqa (F811)


admin.site.site_title = _('Сайт')
admin.site.site_header = _('Сайт')
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
