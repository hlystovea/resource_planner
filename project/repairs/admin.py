from django.contrib import admin
from django.db.models import CharField, TextField
from django.forms import Textarea, TextInput
from django.utils.translation import gettext_lazy as _

from .models import Object, Operation, Repair


class MixinAdmin(admin.ModelAdmin):
    empty_value_display = _('-пусто-')
    formfield_overrides = {
        CharField: {'widget': TextInput(attrs={'size': 80})},
        TextField: {'widget': Textarea(attrs={'rows': 8, 'cols': 80})},
    }


@admin.register(Object)
class ObjectAdmin(MixinAdmin):
    list_display = ('id', 'name', 'inventory_number')
    search_fields = ('name', 'inventory_number')


@admin.register(Operation)
class OperationAdmin(MixinAdmin):
    list_display = ('id', 'name', 'man_hours')
    search_fields = ('name', )


@admin.register(Repair)
class RepairAdmin(MixinAdmin):
    list_display = ('id', 'name', 'object', 'start_time', 'end_time')
    search_fields = ('name', )
    autocomplete_fields = ('object', )
