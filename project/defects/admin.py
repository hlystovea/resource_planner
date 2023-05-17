from django.contrib import admin
from django.db.models import CharField, TextField
from django.forms import Textarea, TextInput
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import (Condition, Defect, Effect, Feature,
                     OrganizationalReason, TechnicalReason)


class MixinAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
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


@admin.register(Defect)
class DefectAdmin(ImageTagField, MixinAdmin):
    list_display = ('id', 'dispatch_object', 'hardware_connection',
                    'hardware_name', 'defect_description', 'defect_repair',
                    'format_date', 'format_repair_date', 'image_tag')
    search_fields = ('description', 'repair')
    list_filter = ('date', 'technical_reasons', 'organizational_reasons')
    autocomplete_fields = ('component', )
    date_hierarchy = 'date'
    readonly_fields = ('employee', )

    @admin.display(description=_('Объект диспетч.'))
    def dispatch_object(self, obj):
        return obj.part.cabinet.hardware.connection.facility

    @admin.display(description=_('Присоединение'))
    def hardware_connection(self, obj):
        return obj.part.cabinet.hardware.connection

    @admin.display(description=_('Оборудование'))
    def hardware_name(self, obj):
        return obj.part.cabinet.hardware.name[:80]

    @admin.display(description=_('Описание'))
    def defect_description(self, obj):
        if obj.description:
            return obj.description[:50]
        return None

    @admin.display(description=_('Мероприятия'))
    def defect_repair(self, obj):
        if obj.repair:
            return obj.repair[:50]
        return None

    @admin.display(description=_('Дата обнаружения'))
    def format_date(self, obj):
        if obj.date:
            return obj.date.strftime('%d.%m.%Y')
        return None

    @admin.display(description=_('Дата устранения'))
    def format_repair_date(self, obj):
        if obj.repair_date:
            return obj.repair_date.strftime('%d.%m.%Y')
        return None

    def lookup_allowed(self, key, value):
        if key in ('component__cabinet__hardware__id__exact', ):
            return True
        return super().lookup_allowed(key, value)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.employee = request.user
        super().save_model(request, obj, form, change)


@admin.register(Condition)
class ConditionAdmin(MixinAdmin):
    pass


@admin.register(Effect)
class EffectAdmin(MixinAdmin):
    pass


@admin.register(Feature)
class FeatureAdmin(MixinAdmin):
    pass


@admin.register(TechnicalReason)
class TechnicalReasonAdmin(MixinAdmin):
    pass


@admin.register(OrganizationalReason)
class OrganizationalReasonAdmin(MixinAdmin):
    pass
