from django.contrib import admin

from apps.wars.models import Meme


class MemeAdminInline(admin.TabularInline):
    model = Meme
    extra = 0
    fields = (
        "war",
        "image",
        "approval_status",
    )
    readonly_fields = (
        "war",
        "image",
    )

    def has_add_permission(self, request, obj) -> bool:
        return False
