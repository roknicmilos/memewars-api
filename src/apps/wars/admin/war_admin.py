from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.common.admin import ModelAdmin
from apps.wars.models import War


@admin.register(War)
class WarAdmin(ModelAdmin):
    list_display = (
        "name",
        "requires_meme_approval",
        "phase",
        "meme_upload_limit",
        "meme_count",
        "voter_count",
        "vote_count",
        "created",
    )
    readonly_fields = (
        "meme_count",
        "voter_count",
        "vote_count",
    )
    add_form_fields = (
        "name",
        "requires_meme_approval",
    )

    @admin.display(description=_("memes"))
    def meme_count(self, obj: War = None) -> int:
        return obj.meme_count

    @admin.display(description=_("voters"))
    def voter_count(self, obj: War = None) -> int:
        return obj.voter_count

    @admin.display(description=_("votes"))
    def vote_count(self, obj: War = None) -> int:
        return obj.vote_count

    def get_readonly_fields(self, request, obj: War = None) -> tuple:
        readonly_fields = super().get_readonly_fields(request=request, obj=obj)
        if not obj or obj.phase != War.Phases.SUBMISSION:
            readonly_fields += ("meme_upload_limit",)
        return readonly_fields
