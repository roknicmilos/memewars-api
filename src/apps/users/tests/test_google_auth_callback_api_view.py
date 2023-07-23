from unittest.mock import patch

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework.authtoken.models import Token

from apps.users.serializers import GoogleAuthCallbackQuerySerializer
from apps.users.tests.factories import UserFactory
from meme_wars.tests import APITestCase


class TestGoogleAuthCallbackAPIView(APITestCase):
    faker = Faker()
    view_serializer_class = GoogleAuthCallbackQuerySerializer

    def setUp(self) -> None:
        super().setUp()
        self._patch_get_or_create_user()
        self._patch_build_login_success_url()
        self._patch_build_login_failure_url()
        self._patch_serializer_is_valid()

    def _patch_get_or_create_user(self) -> None:
        self.get_or_create_user_patcher = patch.object(self.view_serializer_class, "get_or_create_user")
        self.mock_get_or_create_user = self.get_or_create_user_patcher.start()

    def _patch_build_login_success_url(self) -> None:
        self.build_login_success_url_patcher = patch.object(self.view_serializer_class, "build_login_success_url")
        self.mock_build_login_success_url = self.build_login_success_url_patcher.start()
        self.mock_build_login_success_url.return_value = self.faker.url()

    def _patch_build_login_failure_url(self) -> None:
        self.build_login_failure_url_patcher = patch.object(self.view_serializer_class, "build_login_failure_url")
        self.mock_build_login_failure_url = self.build_login_failure_url_patcher.start()
        self.mock_build_login_failure_url.return_value = self.faker.url()

    def _patch_serializer_is_valid(self) -> None:
        self.serializer_is_valid_patcher = patch.object(self.view_serializer_class, "is_valid")
        self.mock_serializer_is_valid = self.serializer_is_valid_patcher.start()
        self.mock_serializer_is_valid.return_value = True

    def test_should_redirect_to_login_success_url_after_creating_new_user(self):
        new_user = UserFactory()
        self.mock_get_or_create_user.return_value = new_user, True

        self.assertFalse(Token.objects.exists())

        response = self.client.get(path=reverse("api:users:google_auth:callback"))

        self.assertEqual(Token.objects.count(), 1)
        self.assertEqual(Token.objects.first().user, new_user)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.mock_build_login_success_url.return_value)

    def test_should_redirect_to_login_success_url_after_getting_existing_user(self):
        exiting_user = UserFactory()
        existing_toke = Token.objects.create(user=exiting_user)
        self.mock_get_or_create_user.return_value = exiting_user, False

        self.assertEqual(Token.objects.count(), 1)

        response = self.client.get(path=reverse("api:users:google_auth:callback"))

        self.assertEqual(Token.objects.count(), 1)
        self.assertFalse(Token.objects.filter(pk=existing_toke.pk).exists())  # old token is deleted
        self.assertEqual(Token.objects.first().user, exiting_user)  # new token is created
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.mock_build_login_success_url.return_value)

    def test_should_redirect_to_login_failure_when_validation_error_is_raised(self):
        self.mock_serializer_is_valid.return_value = False

        response = self.client.get(path=reverse("api:users:google_auth:callback"))

        self.assertFalse(Token.objects.exists())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.mock_build_login_failure_url.return_value)

    def test_should_raise_error_when_get_or_create_user_raises_error(self):
        error_message = "get_or_create_user exception"
        self.mock_get_or_create_user.side_effect = ValueError(error_message)

        with pytest.raises(expected_exception=ValueError, match=error_message):
            self.client.get(path=reverse("api:users:google_auth:callback"))

    def tearDown(self) -> None:
        super().tearDown()
        self.get_or_create_user_patcher.stop()
        self.build_login_success_url_patcher.stop()
        self.build_login_failure_url_patcher.stop()
        self.serializer_is_valid_patcher.stop()
        Token.objects.all().delete()
