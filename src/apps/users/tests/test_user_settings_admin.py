from django.contrib.admin.sites import site as admin_site
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from apps.users.admin import UserSettingsAdmin
from apps.users.models import UserSettings
from meme_wars.tests.test_case import TestCase
from meme_wars.utils import get_model_admin_change_details_url


class TestUserSettingsAdmin(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user_settings_admin = UserSettingsAdmin(model=UserSettings, admin_site=admin_site)
        user_settings_content_type = ContentType.objects.get_for_model(UserSettings)
        self.user_settings_app_label = user_settings_content_type.app_label
        self.user_settings_model = user_settings_content_type.model

    def test_should_not_allow_to_add_new_objects(self):
        self.assertFalse(self.user_settings_admin.has_add_permission(request=self.get_request_example()))

    def test_should_not_allow_to_delete_objects(self):
        self.assertFalse(self.user_settings_admin.has_delete_permission(request=self.get_request_example()))

    def test_should_redirect_from_list_view_to_details_view(self):
        # When UserSettings does not exist, it should be created before the redirect
        self.assertFalse(UserSettings.exists())
        list_url_path = reverse(viewname=f"admin:{self.user_settings_app_label}_{self.user_settings_model}_changelist")
        self.create_and_login_superuser()
        response = self.client.get(path=list_url_path)
        self.assertTrue(UserSettings.exists())
        details_url_path = get_model_admin_change_details_url(obj=UserSettings.load())
        assertRedirects(response, details_url_path)

    def test_should_create_user_settings_when_accessing_details_view_and_user_settings_do_not_exist(self):
        self.assertFalse(UserSettings.exists())
        self.create_and_login_superuser()
        details_url_path = reverse(
            viewname=f"admin:{self.user_settings_app_label}_{self.user_settings_model}_change", args=(1,)
        )
        response = self.client.get(path=details_url_path)
        self.assertTrue(UserSettings.exists())
        self.assertTrue(response.status_code, 200)
