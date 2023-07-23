from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.db.models import QuerySet
from django.db.models.functions import Collate
from django.utils.translation import gettext_lazy as _

from apps.common.admin import ModelAdmin
from apps.users.admin import MemeAdminInline
from apps.users.models import User

admin.site.unregister(Group)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (User.USERNAME_FIELD,)


@admin.register(User)
class UserAdmin(ModelAdmin, BaseUserAdmin):
    list_display = (
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    search_fields = ("first_name", "last_name", "email_deterministic")
    ordering = ("email",)
    inlines = (MemeAdminInline,)
    add_form = CreateUserForm
    fieldsets = (
        (None, {"fields": ("id", "email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {
                "fields": (
                    "last_login",
                    "date_joined",
                    "created",
                    "modified",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    readonly_fields = (
        "last_login",
        "date_joined",
    )

    def get_queryset(self, request) -> QuerySet:
        queryset = super().get_queryset(request)
        return queryset.annotate(email_deterministic=Collate("email", "und-x-icu"))

    def get_inlines(self, request, obj: User = None) -> tuple:
        return super().get_inlines(request=request, obj=obj) if obj else ()
