from django.contrib import admin
from django.db.models import CharField, TextField
from django.forms import Textarea, TextInput
from django.utils.translation import gettext_lazy as _

from .models import Protocol, ProtocolE2, Template


class MixinAdmin(admin.ModelAdmin):
    empty_value_display = _('-пусто-')
    formfield_overrides = {
        CharField: {'widget': TextInput(attrs={'size': 80})},
        TextField: {'widget': Textarea(attrs={'rows': 8, 'cols': 80})},
    }


@admin.register(ProtocolE2)
class ProtocolE2Admin(MixinAdmin):
    list_display = ('id', 'date', 'connection', 'supervisor')
    list_filter = ('date', 'connection')
    date_hierarchy = 'date'


@admin.register(Protocol)
class ProtocolAdmin(MixinAdmin):
    list_display = ('id', 'date', 'connection', 'supervisor')
    list_filter = ('date', 'connection')
    date_hierarchy = 'date'


@admin.register(Template)
class TemplateAdmin(MixinAdmin):
    list_display = ('id', 'name')
