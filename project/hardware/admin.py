from django.contrib import admin
from django.db.models import CharField, TextField
from django.forms import Textarea, TextInput
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _

from .models import (Cabinet, Component, ComponentDesign,
                     ComponentFunction, ComponentRepairMethod,
                     Connection, Facility, Group, Hardware,
                     Manufacturer, Part)
from defects.models import Defect


class MixinAdmin(admin.ModelAdmin):
    search_fields = ('name', )
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


class PartInline(admin.TabularInline):
    model = Part
    show_change_link = True
    verbose_name_plural = _('Входящие в состав комплектующие')
    readonly_fields = ('cabinet', )


@admin.register(Part)
class PartAdmin(MixinAdmin):
    list_display = ('id', 'name', 'component', 'get_cabinet',
                    'get_part', 'release_year', 'launch_year')
    list_filter = ('component__design', 'component__repair_method',
                   'launch_year')
    autocomplete_fields = ('component', 'part', 'cabinet')
    inlines = (PartInline, )

    @admin.display(description=_('Шкаф/Панель'))
    def get_cabinet(self, obj):
        if obj.cabinet:
            url = (
                reverse(
                    'admin:hardware_cabinet_change',
                    args=(obj.cabinet.id, )
                )
            )
            return format_html('<a href="{}">{}</a>', url, obj.cabinet)
        return ''

    @admin.display(description=_('Комплектующее'))
    def get_part(self, obj):
        if obj.part:
            url = (
                reverse(
                    'admin:hardware_part_change',
                    args=(obj.part.id, )
                )
            )
            return format_html('<a href="{}">{}</a>', url, obj.part)
        return ''

    def save_formset(self, request, form, formset, change) -> None:
        instances = formset.save(commit=False)
        for instance in instances:
            instance.cabinet = form.cleaned_data['cabinet']
            instance.save()


@admin.register(Component)
class ComponentAdmin(MixinAdmin):
    list_display = ('id', 'name', 'manufacturer', 'design', 'series', 'type')
    list_filter = ('design', 'function', 'repair_method')


@admin.register(Cabinet)
class CabinetAdmin(MixinAdmin):
    list_display = ('id', 'abbreviation', 'hardware',
                    'release_year', 'launch_year')
    list_filter = ('hardware__connection__facility',
                   'hardware__connection', 'launch_year')
    autocomplete_fields = ('hardware', )
    inlines = (PartInline, )


class CabinetInline(admin.TabularInline):
    model = Cabinet
    show_change_link = True
    verbose_name_plural = _('Входящие в состав шкафы/панели')


@admin.register(Hardware)
class HardwareAdmin(MixinAdmin):
    list_display = ('id', 'facility', 'connection', 'name',
                    'inventory_number', 'count_defects')
    search_fields = ('name', 'inventory_number')
    list_filter = ('connection__facility', 'connection')
    inlines = (CabinetInline, )

    @admin.display(description=_('Объект дисп.'))
    def facility(self, obj):
        return obj.connection.facility

    @admin.display(description=_('Кол-во дефектов'))
    def count_defects(self, obj):
        url = (
            reverse('admin:defects_defect_changelist')
            + '?'
            + urlencode({'component__cabinet__hardware__id__exact': obj.id})
        )
        return format_html(
            '<a href="{}">{}</a>',
            url,
            Defect.objects.filter(component__cabinet__hardware=obj).count()
        )


class HardwareInline(admin.TabularInline):
    model = Hardware
    show_change_link = True


@admin.register(Connection)
class ConnectionAdmin(MixinAdmin):
    list_display = ('id', 'facility', 'name', 'abbreviation')
    list_filter = ('facility', )
    autocomplete_fields = ('facility', )
    inlines = (HardwareInline, )


class ConnectionInline(admin.TabularInline):
    model = Connection
    show_change_link = True


@admin.register(Facility)
class FacilityAdmin(MixinAdmin):
    list_display = ('id', 'name', 'abbreviation', 'count_connections')
    inlines = (ConnectionInline, )

    @admin.display(description=_('Кол-во присоединений'))
    def count_connections(self, obj):
        url = (
            reverse('admin:hardware_connection_changelist')
            + '?'
            + urlencode({'facility__id': obj.id})
        )
        return format_html(
            '<a href="{}">{}</a>', url, obj.connections.count()
        )


@admin.register(Group)
class GroupAdmin(MixinAdmin):
    list_display = ('id', 'name', 'count_hardware')

    @admin.display(description=_('Кол-во оборудования'))
    def count_hardware(self, obj):
        url = (
            reverse('admin:hardware_hardware_changelist')
            + '?'
            + urlencode({'group__id': obj.id})
        )
        return format_html(
            '<a href="{}">{}</a>', url, obj.hardware.count()
        )


@admin.register(ComponentDesign)
class ComponentDesignAdmin(MixinAdmin):
    pass


@admin.register(ComponentRepairMethod)
class ComponentRepairMethodAdmin(MixinAdmin):
    pass


@admin.register(ComponentFunction)
class ComponentFunctionAdmin(MixinAdmin):
    pass


@admin.register(Manufacturer)
class ManufacturerAdmin(MixinAdmin):
    pass
