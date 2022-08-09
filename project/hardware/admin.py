from django.contrib import admin
from django.db.models import CharField, TextField
from django.forms import Textarea, TextInput
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _

from .models import Connection, Facility, Hardware


class MixinAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'abbreviation')
    empty_value_display = _('-пусто-')
    formfield_overrides = {
        CharField: {'widget': TextInput(attrs={'size': 80})},
        TextField: {'widget': Textarea(attrs={'rows': 8, 'cols': 80})},
    }


class ImageTagField(admin.ModelAdmin):
    readonly_fields = ('image_tag',)

    @admin.display(description=_('Фотография'))
    def image_tag(self, instance):
        if instance.image:
            return format_html(
                '<img src="{0}" style="max-height: 50px"/>',
                instance.image.url
            )
        return None


@admin.register(Hardware)
class HardwareAdmin(MixinAdmin):
    list_display = ('id', 'facility', 'connection', 'name',
                    'inventory_number', 'count_defects')
    search_fields = ('name', 'inventory_number')
    list_filter = ('facility', 'connection', )

    @admin.display(description=_('Кол-во дефектов'))
    def count_defects(self, obj):
        count = obj.defects.count()
        url = (
            reverse('admin:defects_defect_changelist')
            + '?'
            + urlencode({'hardware__id': f'{obj.id}'})
        )
        return format_html(
            '<a href="{}">{}</a>', url, count
        )


@admin.register(Connection)
class ConnectionAdmin(MixinAdmin):
    pass


@admin.register(Facility)
class FacilityAdmin(MixinAdmin):
    pass
