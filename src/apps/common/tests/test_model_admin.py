from unittest.mock import patch

from django.contrib.admin.options import BaseModelAdmin
from django.contrib.admin.sites import site as admin_site
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from apps.common.admin import ModelAdmin, TimestampableModelAdmin
from meme_wars.tests.test_case import TestCase


class TestModelAdmin(TestCase):
    class UserAdmin(ModelAdmin):
        pass

    def setUp(self) -> None:
        super().setUp()
        self.user_admin = self.UserAdmin(model=User, admin_site=admin_site)

    def test_should_return_add_form_fields(self):
        self.UserAdmin.add_form_fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        )
        actual_fieldsets = self.user_admin.get_fields(request=self.get_request_example())
        self.assertEqual(actual_fieldsets, self.UserAdmin.add_form_fields)
        self.UserAdmin.add_form_fields = None  # Revert changes added in this test to UserAdmin class

    def test_should_return_change_form_fields(self):
        self.UserAdmin.change_form_fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
        )
        actual_fieldsets = self.user_admin.get_fields(request=self.get_request_example(), obj=User())
        self.assertEqual(actual_fieldsets, self.UserAdmin.change_form_fields)
        self.UserAdmin.change_form_fields = None  # Revert changes added in this test to UserAdmin class

    @patch.object(BaseModelAdmin, "formfield_for_manytomany", return_value=None)
    def test_should_return_default_fields(self, _):
        # When User object is not passed to the function:
        actual_fields = self.user_admin.get_fields(request=self.get_request_example())
        expected_fields = (
            "id",
            "password",
            "last_login",
            "is_superuser",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
        )
        expected_fields += TimestampableModelAdmin.timestampable_fields
        self.assertEqual(actual_fields, expected_fields)

        # When User object is passed to the function:
        actual_fields = self.user_admin.get_fields(request=self.get_request_example(), obj=User())
        self.assertEqual(actual_fields, expected_fields)

    def test_should_return_add_form_fieldsets(self):
        self.UserAdmin.add_form_fieldsets = (
            (
                None,
                {
                    "fields": (
                        "id",
                        "username",
                    )
                },
            ),
            (
                "Optional",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "email",
                    )
                },
            ),
        )
        actual_fieldsets = self.user_admin.get_fieldsets(request=self.get_request_example())
        self.assertEqual(actual_fieldsets, self.UserAdmin.add_form_fieldsets)
        self.UserAdmin.add_form_fieldsets = None  # Revert changes added in this test to UserAdmin class

    def test_should_return_change_form_fieldsets(self):
        self.UserAdmin.change_form_fieldsets = (
            (
                None,
                {
                    "fields": (
                        "id",
                        "username",
                        "first_name",
                        "last_name",
                        "email",
                    )
                },
            ),
            (
                "Additional",
                {
                    "fields": (
                        "is_staff",
                        "is_active",
                        "date_joined",
                    )
                },
            ),
        )
        actual_fieldsets = self.user_admin.get_fieldsets(request=self.get_request_example(), obj=User())
        self.assertEqual(actual_fieldsets, self.UserAdmin.change_form_fieldsets)
        self.UserAdmin.change_form_fieldsets = None  # Revert changes added in this test to UserAdmin class

    @patch.object(BaseModelAdmin, "formfield_for_manytomany", return_value=None)
    def test_should_return_default_fieldsets(self, _):
        # When User object is not passed to the function:
        actual_fieldsets = self.user_admin.get_fieldsets(request=self.get_request_example())
        expected_fieldsets = [
            (
                None,
                {
                    "fields": (
                        "id",
                        "password",
                        "last_login",
                        "is_superuser",
                        "username",
                        "first_name",
                        "last_name",
                        "email",
                        "is_staff",
                        "is_active",
                        "date_joined",
                        *TimestampableModelAdmin.timestampable_fields,
                    )
                },
            )
        ]
        self.assertEqual(actual_fieldsets, expected_fieldsets)

        # When User object is passed to the function:
        actual_fieldsets = self.user_admin.get_fieldsets(request=self.get_request_example(), obj=User())
        self.assertEqual(actual_fieldsets, expected_fieldsets)

    def test_should_return_correct_admin_id_string_when_object_is_passed(self):
        user_class = get_user_model()
        user = user_class.objects.create()
        actual_admin_id = self.user_admin.admin_id(obj=user)
        self.assertEqual(actual_admin_id, f"{user.verbose_name} {user.pk}")
