from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.db.models import CharField, Sum, TextField
from django.forms import Textarea, TextInput
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _

from .models import Dept, Service

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


@admin.register(Service)
class ServiceAdmin(MixinAdmin):
    list_display = ('id', 'abbreviation', 'name', 'headcount')
    search_fields = ('name', 'abbreviation')

    @admin.display(description=_('Численность'))
    def headcount(self, obj):
        headcount = obj.departments.aggregate(total=Sum('employees'))
        url = (
            reverse('admin:staff_employee_changelist')
            + '?'
            + urlencode({'service__id': f'{obj.id}'})
        )
        return format_html(
            '<a href="{}">{} чел.</a>', url, headcount['total'] or 0
        )


@admin.register(Dept)
class DeptAdmin(MixinAdmin):
    list_display = ('id', 'abbreviation', 'name', 'headcount',
                    'materials_count', 'instrument_count')
    search_fields = ('name', 'abbreviation')
    list_filter = ('service', )

    @admin.display(description=_('Численность'))
    def headcount(self, obj):
        headcount = obj.employees.count()
        url = (
            reverse('admin:staff_employee_changelist')
            + '?'
            + urlencode({'dept__id': f'{obj.id}'})
        )
        return format_html(
            '<a href="{}">{} чел.</a>', url, headcount or 0
        )

    @admin.display(description=_('Материалы'))
    def materials_count(self, obj):
        materials_count = obj.materials.count()
        url = (
            reverse('admin:warehouse_materialstorage_changelist')
            + '?'
            + urlencode({'owner__id': f'{obj.id}'})
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
            + urlencode({'owner__id': f'{obj.id}'})
        )
        return format_html(
            '<a href="{}">{} поз.</a>', url, instrument_count
        )


@admin.register(User)
class EmployeeAdmin(UserAdmin):
    empty_value_display = _('-пусто-')
    list_display = ('id', 'last_name', 'first_name',
                    'patronymic', 'dept', 'is_chief')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('dept', 'dept__service', 'is_chief',
                   'is_staff', 'is_active', 'is_superuser')
    autocomplete_fields = ('dept', )
    readonly_fields = ('date_joined', 'last_login')

    add_fieldsets = (
        (_('Логин/пароль'), {
            'fields': ('username', )
        }),
        (_('Персональная информация'), {
            'fields': (
                ('first_name', 'last_name', 'patronymic'), 'email', 'dept'
            )
        }),
        (_('Права доступа'), {
            'fields': (
                'is_active', 'is_staff', 'is_chief', 'is_superuser', 'groups'
            )
        }),
        (_('Даты последнего входа/регистрации'), {
            'fields': ('last_login', 'date_joined')
        })
    )

    fieldsets = (
        (_('Логин/пароль'), {
            'fields': ('username', 'password')
        }),
        (_('Персональная информация'), {
            'fields': (
                ('first_name', 'last_name', 'patronymic'), 'email', 'dept'
            )
        }),
        (_('Права доступа'), {
            'fields': (
                'is_active', 'is_staff', 'is_chief', 'is_superuser', 'groups'
            )
        }),
        (_('Даты последнего входа/регистрации'), {
            'fields': ('last_login', 'date_joined')
        })
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()
        if not is_superuser:
            disabled_fields |= {
                'is_superuser',
                'user_permissions',
            }
        if (
            not is_superuser
            and obj is not None
            and (obj.is_superuser or obj == request.user)
        ):
            disabled_fields |= {
                'is_active',
                'is_staff',
                'is_chief',
                'is_superuser',
                'groups',
                'user_permissions',
            }
        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
        return form
