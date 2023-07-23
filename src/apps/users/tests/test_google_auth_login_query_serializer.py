from unittest.mock import patch

from faker import Faker

from apps.users.models import LoginInProgress
from apps.users.serializers import (
    GoogleAuthLoginQuerySerializer,
    google_auth_login_query_serializer,
)
from meme_wars.tests.test_case import TestCase


class TestGoogleAuthLoginQuerySerializer(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.valid_data = {
            "login_success_redirect_url": Faker().url(),
            "login_failure_redirect_url": Faker().url(),
        }

    def test_should_return_validation_error_for_invalid_query_params(self):
        # When URL query params are missing:
        request = self.get_request_example()
        serializer = GoogleAuthLoginQuerySerializer(request=request)
        serializer.is_valid()
        expected_errors = {
            "login_success_redirect_url": [self.ValidationErrorMessages.REQUIRED_FIELD_ERROR_MSG],
            "login_failure_redirect_url": [self.ValidationErrorMessages.REQUIRED_FIELD_ERROR_MSG],
        }
        self.assertSerializerErrors(serializer, expected_errors)

        # When URL query params contain invalid values:
        url_query_params = {"login_success_redirect_url": "invalid-url", "login_failure_redirect_url": "invalid-url"}
        request = self.get_request_example(url_query_params=url_query_params)
        serializer = GoogleAuthLoginQuerySerializer(request=request)
        serializer.is_valid()
        expected_errors["login_success_redirect_url"] = [self.ValidationErrorMessages.INVALID_URL_ERROR_MSG]
        expected_errors["login_failure_redirect_url"] = [self.ValidationErrorMessages.INVALID_URL_ERROR_MSG]
        self.assertSerializerErrors(serializer, expected_errors)

    def test_should_save_login_data_to_session_when_data_is_valid(self):
        request = self.get_request_example(url_query_params=self.valid_data)
        serializer = GoogleAuthLoginQuerySerializer(request=request)
        self.assertTrue(serializer.is_valid())
        login_in_progress_dict = serializer.request.session[LoginInProgress.session_key]
        self.assertIsInstance(login_in_progress_dict["google_auth_state"], str)
        self.assertEqual(
            login_in_progress_dict["login_success_redirect_url"], self.valid_data["login_success_redirect_url"]
        )
        self.assertEqual(
            login_in_progress_dict["login_failure_redirect_url"], self.valid_data["login_failure_redirect_url"]
        )

    @patch.object(google_auth_login_query_serializer, "build_google_login_url")
    def test_should_get_login_url(self, mock_build_google_login_url):
        mock_build_google_login_url.return_value = "http://google-login-url/"
        request = self.get_request_example(url_query_params=self.valid_data)
        serializer = GoogleAuthLoginQuerySerializer(request=request)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.login_url, mock_build_google_login_url.return_value)
        self.assertIn(LoginInProgress.session_key, serializer.request.session)
