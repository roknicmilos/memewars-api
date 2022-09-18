from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from apps.common.admin import ModelAdmin
from apps.meme_wars.models import Enlistment, Meme


class MemeInline(admin.TabularInline):
    model = Meme
    extra = 0


@admin.register(Enlistment)
class EnlistmentAdmin(ModelAdmin):
    search_fields = ('user__email', 'war__name',)
    list_display = ('self_str', 'user', 'war',)
    readonly_fields = ('self_str', 'created', 'modified',)
    add_form_fields = ('user', 'war',)
    inlines = [
        MemeInline,
    ]

    def self_str(self, obj: Meme = None) -> str:
        return str(obj)

    self_str.short_description = _('enlistment')
