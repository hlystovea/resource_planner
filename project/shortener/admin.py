from django.contrib import admin
from django.db.models import CharField, TextField
from django.forms import Textarea, TextInput
from django.utils.translation import gettext_lazy as _

from .models import Shortener


class ShortenerYearFilter(admin.SimpleListFilter):
    title = _('год')
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        dates = Shortener.objects.dates('created_at', 'year')
        return [(d.year, d.year) for d in dates]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(created_at__year=self.value())
        return queryset


class MixinAdmin(admin.ModelAdmin):
    empty_value_display = _('-пусто-')
    formfield_overrides = {
        CharField: {'widget': TextInput(attrs={'size': 80})},
        TextField: {'widget': Textarea(attrs={'rows': 8, 'cols': 80})},
    }


@admin.register(Shortener)
class ShortenerAdmin(MixinAdmin):
    list_display = ('id', 'short_url', 'long_url', 'format_created_at')
    search_fields = ('short_url', 'long_url')
    list_filter = ('created_at', ShortenerYearFilter)

    @admin.display(description=_('Время создания'))
    def format_created_at(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M:%S')
