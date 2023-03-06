from django.contrib.admin.sites import site as admin_site
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from apps.common.tests import TestCase
from apps.common.utils import get_model_admin_change_details_url
from apps.users.admin import UserSettingsAdmin
from apps.users.models import UserSettings


class TestModelAdmin(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.user_settings_admin = UserSettingsAdmin(model=UserSettings, admin_site=admin_site)

    def test_should_not_allow_to_add_new_objects(self):
        self.assertFalse(self.user_settings_admin.has_add_permission(request=self.get_request_example()))

    def test_should_not_allow_to_delete_objects(self):
        self.assertFalse(self.user_settings_admin.has_delete_permission(request=self.get_request_example()))

    def test_should_redirect_from_list_view_to_details_view(self):
        # When UserSettings does not exist, it should be created before the redirect
        self.assertFalse(UserSettings.exists())
        content_type = ContentType.objects.get_for_model(UserSettings)
        list_url_path = reverse(f'admin:{content_type.app_label}_{content_type.model}_changelist')
        self.create_and_login_superuser()
        response = self.client.get(path=list_url_path)
        self.assertTrue(UserSettings.exists())
        details_url_path = get_model_admin_change_details_url(obj=UserSettings.load())
        assertRedirects(response, details_url_path)
