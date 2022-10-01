from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from apps.common.admin import ModelAdmin
from apps.meme_wars.models import Meme


@admin.register(Meme)
class MemeAdmin(ModelAdmin):
    search_fields = (
        'enlistment__user__email',
        'enlistment__user__first_name',
        'enlistment__user__last_name',
        'enlistment__war__name',
    )
    list_display = ('admin_id', 'image', 'user', 'enlistment', 'war', 'vote_count', 'total_score',)
    add_form_fields = ('enlistment', 'image',)

    def admin_id(self, obj: Meme = None) -> str:
        return _(f'Meme {obj.pk}') if obj else None

    admin_id.short_description = _('id')

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(MemeAdmin, self).get_readonly_fields(request=request, obj=obj)
        if obj and obj.pk:
            readonly_fields += ('enlistment',)
        return readonly_fields

    def has_change_permission(self, request, obj=None):
        return False
