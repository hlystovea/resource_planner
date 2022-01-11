from django.contrib import admin
from django.db.models import CharField, Sum, TextField
from django.forms import Textarea, TextInput
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _

from .models import InstrumentSheet, MaterialSheet, OperationSheet, Sheet


class MixinAdmin(admin.ModelAdmin):
    empty_value_display = _('-пусто-')
    formfield_overrides = {
        CharField: {'widget': TextInput(attrs={'size': 80})},
        TextField: {'widget': Textarea(attrs={'rows': 8, 'cols': 80})},
    }


class OperationSheetInline(admin.TabularInline):
    model = OperationSheet
    autocomplete_fields = ('operation', )
    min_num = 1
    extra = 0


class InstrumentSheetInline(admin.TabularInline):
    model = InstrumentSheet
    autocomplete_fields = ('instrument', )
    min_num = 1
    extra = 0


class MaterialSheetInline(admin.TabularInline):
    model = MaterialSheet
    autocomplete_fields = ('material', )
    min_num = 1
    extra = 0


@admin.register(Sheet)
class SheetAdmin(MixinAdmin):
    list_display = ('id', 'name', 'object', 'total_man_hours')
    search_fields = ('name', 'object')
    inlines = [
        OperationSheetInline,
        InstrumentSheetInline,
        MaterialSheetInline,
    ]

    @admin.display(description=_('Суммарные трудозатраты'))
    def total_man_hours(self, obj):
        man_hours = obj.operations.aggregate(total=Sum('operation__man_hours'))
        url = (
            reverse('admin:repairs_operation_changelist')
            + '?'
            + urlencode({'sheet__id': f'{obj.id}'})
        )
        return format_html(
            '<a href="{}">{} чел./ч</a>', url, man_hours.get('total')
        )
