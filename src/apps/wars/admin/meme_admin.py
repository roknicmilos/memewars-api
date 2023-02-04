from django.contrib import admin
from apps.common.admin import ModelAdmin
from apps.wars.admin.forms import MemeAdminForm
from apps.wars.models import Meme


@admin.register(Meme)
class MemeAdmin(ModelAdmin):
    form = MemeAdminForm
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
    fields = (
        'id', 'user', 'war', 'image', 'is_approved',
    )
    readonly_fields = (
        'user', 'war', 'is_approved',
    )
