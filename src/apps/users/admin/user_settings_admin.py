from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect

from apps.common.admin import ModelAdmin
from apps.users.forms import UserSettingsAdminForm
from apps.users.models import UserSettings
from meme_wars.utils import get_model_admin_change_details_url


@admin.register(UserSettings)
class UserSettingsAdmin(ModelAdmin):
    form = UserSettingsAdminForm

    def has_add_permission(self, request) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def changelist_view(self, request, extra_context=None) -> HttpResponseRedirect:
        details_url = get_model_admin_change_details_url(obj=UserSettings.load())
        return HttpResponseRedirect(redirect_to=details_url)

    def change_view(self, request, object_id, form_url="", extra_context=None) -> HttpResponse:
        if not UserSettings.exists():
            UserSettings.load()
        return super().change_view(request, object_id, form_url, extra_context)
