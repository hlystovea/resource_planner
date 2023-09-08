import csv
from django.contrib import admin
from django.db.models import CharField, F, TextField
from django.forms import Textarea, TextInput
from django.http import HttpResponse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import (Condition, Defect, Effect, Feature,
                     OrganizationalReason, RepairMethod,
                     TechnicalReason)


class ExportCsvMixin(admin.ModelAdmin):
    def export_as_csv(self, request, queryset):
        meta = self.model._meta

        if not hasattr(self, 'list_csv_export'):
            self.list_csv_export = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'

        writer = csv.writer(response)
        writer.writerow(self.list_csv_export)

        for obj in queryset:
            result = []

            for field in self.list_csv_export:
                attr = getattr(obj, field, None)

                if attr and attr.__class__.__name__ == 'ManyRelatedManager':
                    result.append(
                        '\n'.join(attr.values_list('name', flat=True))
                    )
                else:
                    result.append(attr)

            writer.writerow(result)

        return response

    export_as_csv.short_description = 'Сохранить выбранные в csv-файл'


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
class DefectAdmin(ImageTagField, MixinAdmin, ExportCsvMixin):
    list_display = ('id', 'dispatch_object', 'hardware_connection',
                    'hardware_name', 'defect_description', 'defect_repair',
                    'format_date', 'format_repair_date', 'image_tag')
    search_fields = ('description', 'repair')
    list_filter = ('date', 'technical_reasons',
                   'organizational_reasons', 'repair_method',
                   'part__cabinet__hardware__group',
                   'part__cabinet__hardware__connection')
    autocomplete_fields = ('part', )
    date_hierarchy = 'date'
    readonly_fields = ('employee', )
    actions = ('export_as_csv',)
    list_csv_export = ('facility_name', 'connection_name', 'hardware_name',
                       'cabinet_name', 'component_name', 'date', 'description',
                       'repair_date', 'repair_method', 'repair', 'employee',
                       'effects', 'features', 'condition', 'technical_reasons',
                       'organizational_reasons')

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
        if key in (
            'part__cabinet__hardware__id__exact',
            'part__cabinet__hardware__group__id__exact',
            'part__cabinet__hardware__connection__id__exact',
            'part__component__id__exact',
            'part__component__manufacturer__id__exact',
        ):
            return True
        return super().lookup_allowed(key, value)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.employee = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            component_name=F('part__component__name'),
            cabinet_name=F('part__cabinet__name'),
            hardware_name=F('part__cabinet__hardware__name'),
            connection_name=F('part__cabinet__hardware__connection__name'),
            facility_name=F('part__cabinet__hardware__connection__facility__name'),  # noqa(E501)
        )


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


@admin.register(RepairMethod)
class RepairMethodAdmin(MixinAdmin):
    pass
