from unittest.mock import patch
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse

from apps.common.tests import TestCase
from apps.users.serializers import GoogleAuthCallbackQuerySerializer
from apps.users.tests.factories import UserFactory
from apps.users.views import google_auth_callback_api_view


class TestGoogleAuthCallbackAPIView(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self._patch_get_or_create_user()
        self._patch_build_login_success_url()
        self._patch_build_login_failure_url()

    def _patch_get_or_create_user(self) -> None:
        self.get_or_create_user_patcher = patch.object(GoogleAuthCallbackQuerySerializer, 'get_or_create_user')
        self.mock_get_or_create_user = self.get_or_create_user_patcher.start()

    def _patch_build_login_success_url(self) -> None:
        self.build_login_success_url_patcher = patch.object(google_auth_callback_api_view, 'build_login_success_url')
        self.mock_build_login_success_url = self.build_login_success_url_patcher.start()
        self.mock_build_login_success_url.return_value = 'https://mock-client-app-domain/mock-login-success-route/'

    def _patch_build_login_failure_url(self) -> None:
        self.build_login_failure_url_patcher = patch.object(google_auth_callback_api_view, 'build_login_failure_url')
        self.mock_build_login_failure_url = self.build_login_failure_url_patcher.start()
        self.mock_build_login_failure_url.return_value = 'https://mock-client-app-domain/mock-login-failure-route/'

    def test_should_return_redirect_to_client_app_success_page_after_creating_new_user(self):
        new_user = UserFactory()
        self.mock_get_or_create_user.return_value = new_user, True

        self.assertFalse(Token.objects.exists())

        response = self.client.get(path=reverse('api:users:google_auth:callback'))

        self.assertEqual(Token.objects.count(), 1)
        self.assertEqual(Token.objects.first().user, new_user)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.mock_build_login_success_url.return_value)

    def test_should_return_redirect_to_client_app_success_page_after_getting_existing_user(self):
        exiting_user = UserFactory()
        existing_toke = Token.objects.create(user=exiting_user)
        self.mock_get_or_create_user.return_value = exiting_user, False

        self.assertEqual(Token.objects.count(), 1)

        response = self.client.get(path=reverse('api:users:google_auth:callback'))

        self.assertEqual(Token.objects.count(), 1)
        self.assertFalse(Token.objects.filter(pk=existing_toke.pk).exists())  # old token is deleted
        self.assertEqual(Token.objects.first().user, exiting_user)  # new token is created
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.mock_build_login_success_url.return_value)

    def test_should_return_redirect_to_client_app_failure_page_after_getting_or_creating_user_fails(self):
        self.mock_get_or_create_user.side_effect = Exception('get_or_create_user exception')

        response = self.client.get(path=reverse('api:users:google_auth:callback'))

        self.assertFalse(Token.objects.exists())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.mock_build_login_failure_url.return_value)

    def tearDown(self) -> None:
        super().tearDown()
        self.get_or_create_user_patcher.stop()
        self.build_login_success_url_patcher.stop()
        self.build_login_failure_url_patcher.stop()
        Token.objects.all().delete()
