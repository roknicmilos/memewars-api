from django.contrib import admin
from django.template.loader import render_to_string
from apps.common.admin import ModelAdmin
from apps.wars.admin.filters import RequiresApprovalFilter
from apps.wars.admin.forms import MemeAdminForm
from apps.wars.models import Meme
from django.utils.translation import gettext_lazy as _


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
        'approval_status',
        RequiresApprovalFilter,
    )
    list_display = (
        'admin_id', 'approval_status_html', 'image', 'user', 'war', 'vote_count', 'total_score',
    )
    add_form_fields = (
        'user', 'war', 'image', 'approval_status',
    )
    fields = (
        'id', 'user', 'war', 'image', 'approval_status',
    )
    readonly_fields = (
        'user', 'war',
    )

    def approval_status_html(self, obj: Meme) -> str:
        return render_to_string(template_name='admin/meme_approval_status.html', context={'meme': obj})

    approval_status_html.short_description = _('approval status')
