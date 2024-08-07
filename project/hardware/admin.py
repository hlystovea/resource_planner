import autocomplete_all
from django.contrib import admin
from django.db.models import CharField, TextField
from django.forms import Textarea, TextInput
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _

from .models import (Cabinet, Component, ComponentDesign,
                     ComponentFunction, Connection, Facility,
                     Group, Hardware, Manufacturer, Part)
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


class PartInline(autocomplete_all.TabularInline):
    model = Part
    show_change_link = True
    verbose_name_plural = _('Входящие в состав комплектующие')
    readonly_fields = ('cabinet', 'part')


@admin.register(Part)
class PartAdmin(MixinAdmin):
    list_display = ('id', 'name', 'component', 'get_cabinet',
                    'get_part', 'release_year', 'launch_year',
                    'comment')
    list_filter = ('component__design', 'launch_year')
    autocomplete_fields = ('component', )
    readonly_fields = ('cabinet', )
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

    def get_form(self, request, obj=None, **kwargs):
        self._obj = obj
        return super().get_form(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'part' and self._obj:
            kwargs['queryset'] = self._obj.cabinet.parts
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_formset(self, request, form, formset, change) -> None:
        instances = formset.save(commit=False)
        for instance in instances:
            instance.cabinet = form.cleaned_data['cabinet']
            instance.save()


@admin.register(Component)
class ComponentAdmin(MixinAdmin):
    list_display = ('id', 'name', 'manufacturer', 'design',
                    'series', 'type', 'defect_count')
    list_filter = ('design', 'function')
    autocomplete_fields = ('manufacturer', )

    @admin.display(description=_('Кол-во дефектов'))
    def defect_count(self, obj):
        url = (
            reverse('admin:defects_defect_changelist')
            + '?'
            + urlencode({'part__component__id__exact': f'{obj.id}'})
        )
        return format_html(
            '<a href="{}">{}</a>',
            url,
            Defect.objects.filter(part__component=obj).count()
        )


@admin.register(Cabinet)
class CabinetAdmin(MixinAdmin):
    list_display = ('id', 'abbreviation', 'name', 'hardware',
                    'release_year', 'launch_year')
    list_filter = ('hardware__connection__facility',
                   'hardware__connection', 'launch_year')
    list_editable = ('hardware', 'release_year', 'launch_year')
    autocomplete_fields = ('hardware', 'manufacturer')
    inlines = (PartInline, )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('parts')


class CabinetInline(autocomplete_all.TabularInline):
    model = Cabinet
    show_change_link = True
    verbose_name_plural = _('Входящие в состав шкафы/панели')


@admin.register(Hardware)
class HardwareAdmin(MixinAdmin):
    list_display = ('id', 'facility', 'connection', 'name',
                    'inventory_number', 'defect_count')
    search_fields = ('name', 'inventory_number')
    list_filter = ('connection__facility', 'connection', 'group')
    inlines = (CabinetInline, )

    @admin.display(description=_('Объект дисп.'))
    def facility(self, obj):
        if obj.connection:
            return obj.connection.facility

    @admin.display(description=_('Кол-во дефектов'))
    def defect_count(self, obj):
        url = (
            reverse('admin:defects_defect_changelist')
            + '?'
            + urlencode({'part__cabinet__hardware__id__exact': f'{obj.id}'})
        )
        return format_html(
            '<a href="{}">{}</a>',
            url,
            Defect.objects.filter(part__cabinet__hardware=obj).count()
        )


class HardwareInline(admin.TabularInline):
    model = Hardware
    show_change_link = True


@admin.register(Connection)
class ConnectionAdmin(MixinAdmin):
    list_display = ('id', 'facility', 'name', 'abbreviation', 'defect_count')
    list_filter = ('facility', )
    autocomplete_fields = ('facility', )
    inlines = (HardwareInline, )

    @admin.display(description=_('Кол-во дефектов'))
    def defect_count(self, obj):
        url = (
            reverse('admin:defects_defect_changelist')
            + '?'
            + urlencode(
                {'part__cabinet__hardware__connection__id__exact': f'{obj.id}'}
            )
        )
        return format_html(
            '<a href="{}">{}</a>',
            url,
            Defect.objects.filter(
                part__cabinet__hardware__connection=obj
            ).count()
        )


class ConnectionInline(admin.TabularInline):
    model = Connection
    show_change_link = True


@admin.register(Facility)
class FacilityAdmin(MixinAdmin):
    list_display = ('id', 'name', 'abbreviation', 'hardware_count')
    inlines = (ConnectionInline, )

    @admin.display(description=_('Кол-во ед. оборудования'))
    def hardware_count(self, obj):
        url = (
            reverse('admin:hardware_hardware_changelist')
            + '?'
            + urlencode({'connection__facility__id': f'{obj.id}'})
        )
        return format_html(
            '<a href="{}">{}</a>',
            url,
            Hardware.objects.filter(
                connection__facility=obj
            ).count()
        )


@admin.register(Group)
class GroupAdmin(MixinAdmin):
    list_display = ('id', 'name', 'hardware_count', 'defect_count')

    @admin.display(description=_('Кол-во ед. оборудования'))
    def hardware_count(self, obj):
        url = (
            reverse('admin:hardware_hardware_changelist')
            + '?'
            + urlencode({'group__id': f'{obj.id}'})
        )
        return format_html(
            '<a href="{}">{}</a>', url, obj.hardware.count()
        )

    @admin.display(description=_('Кол-во дефектов'))
    def defect_count(self, obj):
        url = (
            reverse('admin:defects_defect_changelist')
            + '?'
            + urlencode(
                {'part__cabinet__hardware__group__id__exact': f'{obj.id}'}
            )
        )
        return format_html(
            '<a href="{}">{}</a>',
            url,
            Defect.objects.filter(
                part__cabinet__hardware__group=obj
            ).count()
        )


@admin.register(ComponentDesign)
class ComponentDesignAdmin(MixinAdmin):
    pass


@admin.register(ComponentFunction)
class ComponentFunctiondmin(MixinAdmin):
    pass


@admin.register(Manufacturer)
class ManufacturerAdmin(MixinAdmin):
    list_display = ('id', 'name', 'defect_count')

    @admin.display(description=_('Кол-во дефектов'))
    def defect_count(self, obj):
        url = (
            reverse('admin:defects_defect_changelist')
            + '?'
            + urlencode(
                {'part__component__manufacturer__id__exact': f'{obj.id}'}
            )
        )
        return format_html(
            '<a href="{}">{}</a>',
            url,
            Defect.objects.filter(part__component__manufacturer=obj).count()
        )
