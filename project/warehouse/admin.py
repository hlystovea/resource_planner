from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import CharField, TextField
from django.forms import Textarea, TextInput
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Material, Instrument

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
    list_filter = ('measurement_unit', )


@admin.register(Instrument)
class InstrumentAdmin(ImageTagField, MixinAdmin):
    list_display = ('id', 'name', 'inventory_number', 'serial_number')
    search_fields = ('name', 'inventory_number', 'serial_number')
