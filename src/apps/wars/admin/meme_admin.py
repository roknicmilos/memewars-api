from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from apps.common.admin import ModelAdmin
from apps.wars.models import Meme


@admin.register(Meme)
class MemeAdmin(ModelAdmin):
    search_fields = (
        'user__email',
        'user__first_name',
        'user__last_name',
        'war__name',
    )
    list_display = ('admin_id', 'image', 'user', 'war', 'vote_count', 'total_score',)
    add_form_fields = ('user', 'war', 'image',)

    def admin_id(self, obj: Meme = None) -> str:
        return _(f'Meme {obj.pk}') if obj else None

    admin_id.short_description = _('id')

    def has_change_permission(self, request, obj=None):
        return False
