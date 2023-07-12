from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin as BaseTokenAdmin
from rest_framework.authtoken.models import Token, TokenProxy

admin.site.unregister(TokenProxy)


@admin.register(Token)
class TokenAdmin(BaseTokenAdmin):
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
    )

    def has_change_permission(self, request, obj=None):
        return False
