from django.contrib import admin
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
    list_filter = (
        'is_approved',
    )
    list_display = (
        'admin_id', 'is_approved', 'image', 'user', 'war', 'vote_count', 'total_score',
    )
    add_form_fields = (
        'user', 'war', 'image', 'is_approved',
    )

    def has_change_permission(self, request, obj=None):
        return False
