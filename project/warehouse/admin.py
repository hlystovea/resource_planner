from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import CharField, TextField
from django.forms import Textarea, TextInput
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _

from .models import Instrument, Material, Storage

User = get_user_model()


class ImageTagField(admin.ModelAdmin):
    readonly_fields = ('image_tag',)

    def image_tag(self, instance):
        if instance.image:
            return format_html(
                '<img src="{0}" style="max-height: 50px"/>',
                instance.image.url
            )
        return None


class MixinAdmin(admin.ModelAdmin):
    empty_value_display = _('-пусто-')
    formfield_overrides = {
        CharField: {'widget': TextInput(attrs={'size': 80})},
        TextField: {'widget': Textarea(attrs={'rows': 8, 'cols': 80})},
    }


@admin.register(Material)
class MaterialAdmin(ImageTagField, MixinAdmin):
    list_display = ('id', 'name', 'measurement_unit',
                    'article_number', 'turnover')
    search_fields = ('name', 'article_number')


@admin.register(Instrument)
class InstrumentAdmin(ImageTagField, MixinAdmin):
    list_display = ('id', 'name', 'inventory_number', 'serial_number')
    search_fields = ('name', 'inventory_number', 'serial_number')


@admin.register(Storage)
class StorageAdmin(MixinAdmin):
    list_display = ('id', 'name', 'parent_storage', 'storage_count',
                    'materials_count', 'instrument_count')
    search_fields = ('name', )

    @admin.display(description=_('Места хранения'))
    def storage_count(self, obj):
        storage_count = obj.storage.count()
        url = (
            reverse('admin:warehouse_storage_changelist')
            + '?'
            + urlencode({'storage__id': f'{obj.id}'})
        )
        return format_html(
            '<a href="{}">{} поз.</a>', url, storage_count
        )

    @admin.display(description=_('Материалы'))
    def materials_count(self, obj):
        materials_count = obj.materials.count()
        url = (
            reverse('admin:warehouse_material_changelist')
            + '?'
            + urlencode({'storage__id': f'{obj.id}'})
        )
        return format_html(
            '<a href="{}">{} поз.</a>', url, materials_count
        )

    @admin.display(description=_('Инструмент/приборы'))
    def instrument_count(self, obj):
        instrument_count = obj.instruments.count()
        url = (
            reverse('admin:warehouse_instrument_changelist')
            + '?'
            + urlencode({'storage__id': f'{obj.id}'})
        )
        return format_html(
            '<a href="{}">{} поз.</a>', url, instrument_count
        )
