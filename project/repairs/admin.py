from django.contrib import admin
from django.db.models import CharField, Sum, TextField
from django.forms import Textarea, TextInput
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _

from .models import (InstrumentSheet, MaterialSheet, Object, Operation,
                     OperationSheet, Repair, Sheet)


class RepairYearFilter(admin.SimpleListFilter):
    title = _('год')
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        dates = Repair.objects.dates('start_at', 'year')
        return [(d.year, d.year) for d in dates]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(start_at__year=self.value())
        return queryset


class RepairMonthFilter(admin.SimpleListFilter):
    title = _('месяц')
    parameter_name = 'month'

    def lookups(self, request, model_admin):
        dates = Repair.objects.dates('start_at', 'month')
        return [(d.month, d.month) for d in dates]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(start_at__month=self.value())
        return queryset


class MixinAdmin(admin.ModelAdmin):
    empty_value_display = _('-пусто-')
    formfield_overrides = {
        CharField: {'widget': TextInput(attrs={'size': 80})},
        TextField: {'widget': Textarea(attrs={'rows': 8, 'cols': 80})},
    }


@admin.register(Object)
class ObjectAdmin(MixinAdmin):
    list_display = ('id', 'connection', 'name', 'inventory_number')
    search_fields = ('name', 'inventory_number')
    list_filter = ('connection', )
    fields = ('name', 'connection', 'inventory_number')


@admin.register(Operation)
class OperationAdmin(MixinAdmin):
    list_display = ('id', 'name', 'man_hours')
    search_fields = ('name', )


@admin.register(Repair)
class RepairAdmin(MixinAdmin):
    list_display = ('id', 'name', 'object', 'loc_start_at', 'loc_end_at')
    search_fields = ('name', )
    list_filter = ('object__connection', 'start_at',
                   RepairYearFilter, RepairMonthFilter)
    autocomplete_fields = ('object', )

    @admin.display(description=_('Время начала'))
    def loc_start_at(self, obj):
        return obj.start_at.strftime('%d.%m.%Y %H:%M')

    @admin.display(description=_('Время окончания'))
    def loc_end_at(self, obj):
        return obj.end_at.strftime('%d.%m.%Y %H:%M')


class OperationSheetInline(admin.TabularInline):
    model = OperationSheet
    autocomplete_fields = ('operation', )
    min_num = 1
    extra = 0


class InstrumentSheetInline(admin.TabularInline):
    model = InstrumentSheet
    autocomplete_fields = ('instrument', )
    extra = 0


class MaterialSheetInline(admin.TabularInline):
    model = MaterialSheet
    autocomplete_fields = ('material', )
    extra = 0


@admin.register(Sheet)
class SheetAdmin(MixinAdmin):
    list_display = ('id', 'name', 'department', 'total_man_hours')
    search_fields = ('name', 'department')
    list_filter = ('department', )
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
            '<a href="{}">{} чел./ч</a>', url, man_hours['total']
        )
