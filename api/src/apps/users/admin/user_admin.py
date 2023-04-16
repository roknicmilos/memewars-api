from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from apps.users.admin import MemeAdminInline
from apps.users.models import User


admin.site.unregister(Group)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (User.USERNAME_FIELD,)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser',)
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    inlines = (
        MemeAdminInline,
    )
    add_form = CreateUserForm
    fieldsets = (
        (None, {'fields': ('id', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions',),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'created', 'modified',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('id', 'last_login', 'date_joined', 'created', 'modified',)
