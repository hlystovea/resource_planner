from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import CharField, TextField
from django.forms import Textarea, TextInput
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _

from .models import Instrument, Material, MaterialStorage, Storage

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
    list_display = ('id', 'name', 'measurement_unit', 'article_number')
    search_fields = ('name', 'article_number')


@admin.register(MaterialStorage)
class MaterialStorageAdmin(MixinAdmin):
    list_display = ('id', 'material', 'inventory_number', 'amount', 'owner')
    search_fields = ('material', 'inventory_number')
    list_filter = ('owner', )
    autocomplete_fields = ('material', )


@admin.register(Instrument)
class InstrumentAdmin(MixinAdmin):
    list_display = ('id', 'name', 'inventory_number', 'serial_number')
    search_fields = ('name', 'inventory_number', 'serial_number')


@admin.register(Storage)
class StorageAdmin(MixinAdmin):
    list_display = ('id', 'name', 'parent_storage',
                    'storage_count', 'materials_count')
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
            reverse('admin:warehouse_materialstorage_changelist')
            + '?'
            + urlencode({'storage__id': f'{obj.id}'})
        )
        return format_html(
            '<a href="{}">{} поз.</a>', url, materials_count
        )
