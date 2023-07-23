from unittest.mock import patch
from urllib.parse import urlencode

from django.urls import reverse_lazy
from faker import Faker

from apps.users.serializers import google_auth_login_query_serializer
from meme_wars.tests import APITestCase


class TestGoogleAuthLoginURLAPIView(APITestCase):
    url_path = reverse_lazy("api:users:google_auth:login")

    def setUp(self) -> None:
        super().setUp()
        self.build_google_login_url_patcher = patch.object(
            target=google_auth_login_query_serializer, attribute="build_google_login_url"
        )
        self.mock_build_google_login_url = self.build_google_login_url_patcher.start()
        self.mock_build_google_login_url.return_value = "https://mock-google/login"

    def test_should_redirect_to_google_login_url(self):
        url_query_params = {
            "login_success_redirect_url": Faker().url(),
            "login_failure_redirect_url": Faker().url(),
        }
        response = self.client.get(path=f"{self.url_path}?{urlencode(url_query_params)}")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.mock_build_google_login_url.return_value)

    def test_should_return_response_400_when_there_is_a_validation_error(self):
        url_query_params = {
            "login_success_redirect_url": "invalid-url",
        }
        response = self.client.get(path=f"{self.url_path}?{urlencode(url_query_params)}")
        self.assertEqual(response.status_code, 400)
        expected_errors = {
            "login_success_redirect_url": [self.ValidationErrorMessages.INVALID_URL_ERROR_MSG],
            "login_failure_redirect_url": [self.ValidationErrorMessages.REQUIRED_FIELD_ERROR_MSG],
        }
        self.assertEqual(response.json(), expected_errors)

    def tearDown(self) -> None:
        super().tearDown()
        self.build_google_login_url_patcher.stop()
