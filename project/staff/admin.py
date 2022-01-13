from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import CharField, Sum, TextField
from django.forms import Textarea, TextInput
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _

from .models import Dept, Service, Staff

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
        headcount = obj.departments.aggregate(total=Sum('staff'))
        url = (
            reverse('admin:staff_staff_changelist')
            + '?'
            + urlencode({'service__id': f'{obj.id}'})
        )
        return format_html(
            '<a href="{}">{} чел.</a>', url, headcount['total'] or 0
        )


@admin.register(Dept)
class DeptAdmin(MixinAdmin):
    list_display = ('id', 'abbreviation', 'name', 'headcount')
    search_fields = ('name', 'abbreviation')
    list_filter = ('service', )

    @admin.display(description=_('Численность'))
    def headcount(self, obj):
        headcount = obj.staff.count()
        url = (
            reverse('admin:staff_staff_changelist')
            + '?'
            + urlencode({'dept__id': f'{obj.id}'})
        )
        return format_html(
            '<a href="{}">{} чел.</a>', url, headcount or 0
        )


@admin.register(Staff)
class StaffAdmin(MixinAdmin):
    list_display = ('id', 'last_name', 'first_name', 'patronymic')
    search_fields = ('last_name', 'first_name', 'patronymic')
    list_filter = ('department__service', 'department')
