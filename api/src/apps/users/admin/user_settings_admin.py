from django.contrib import admin
from django.http import HttpResponseRedirect

from apps.common.admin import ModelAdmin
from apps.common.utils import get_model_admin_change_details_url
from apps.users.models import UserSettings


@admin.register(UserSettings)
class UserSettingsAdmin(ModelAdmin):

    def has_add_permission(self, request) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def changelist_view(self, request, extra_context=None) -> HttpResponseRedirect:
        details_url = get_model_admin_change_details_url(obj=UserSettings.load())
        return HttpResponseRedirect(redirect_to=details_url)
