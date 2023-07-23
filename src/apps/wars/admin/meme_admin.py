from django.contrib import admin
from django.db.models import QuerySet
from django.db.models.functions import Collate
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from apps.common.admin import ModelAdmin
from apps.wars.admin.filters import RequiresApprovalFilter
from apps.wars.admin.forms import MemeAdminForm
from apps.wars.models import Meme


@admin.register(Meme)
class MemeAdmin(ModelAdmin):
    form = MemeAdminForm
    search_fields = (
        "user_email_deterministic",
        "user__first_name",
        "user__last_name",
        "war__name",
    )
    list_filter = (
        "approval_status",
        RequiresApprovalFilter,
    )
    list_display = (
        "admin_id",
        "approval_status_html",
        "image",
        "user",
        "war",
        "vote_count",
        "total_score",
    )
    add_form_fields = (
        "user",
        "war",
        "image",
        "approval_status",
    )
    fields = (
        "id",
        "user",
        "war",
        "image",
        "approval_status",
        "total_score",
    )

    def get_queryset(self, request) -> QuerySet:
        queryset = super().get_queryset(request)
        return queryset.annotate(user_email_deterministic=Collate("user__email", "und-x-icu"))

    def get_readonly_fields(self, request, obj=None) -> tuple:
        readonly_fields = super().get_readonly_fields(request=request, obj=obj)
        if obj:
            return readonly_fields + (
                "user",
                "war",
                "total_score",
            )
        return readonly_fields

    @admin.display(description=_("approval status"))
    def approval_status_html(self, obj: Meme) -> str:
        return render_to_string(template_name="admin/meme_approval_status.html", context={"meme": obj})
