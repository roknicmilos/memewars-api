from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from apps.common.admin import ModelAdmin
from meme_wars.utils import get_model_admin_change_details_url
from apps.wars.models import Vote


@admin.register(Vote)
class VoteAdmin(ModelAdmin):
    list_display = (
        'admin_id', 'user', 'meme_id', 'score', 'submission_count', 'war', 'created', 'modified',
    )
    search_fields = (
        'user__email',
        'user__first_name',
        'user__last_name',
        'meme__pk',
        'meme__war__name',
    )
    fields = (
        'user', 'meme', 'score', 'submission_count', 'war', 'created', 'modified',
    )

    @admin.display(description=_('meme'))
    def meme_id(self, obj: Vote = None) -> int | None:
        meme_admin_url = get_model_admin_change_details_url(obj=obj.meme)
        label = _(f'Meme {obj.meme.pk}')
        html_link = f'<a href="{meme_admin_url}">{label}</a>'
        return mark_safe(html_link)  # nosec B703, B308

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
