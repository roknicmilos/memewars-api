import re
from unittest.mock import patch
from urllib import parse
from uuid import uuid4

import pytest
from django.conf import settings
from faker import Faker
from rest_framework.authtoken.models import Token

from apps.users.models import LoginInProgress, UserSettings
from apps.users.serializers import (
    GoogleAuthCallbackQuerySerializer,
    google_auth_callback_query_serializer,
)
from apps.users.tests.factories import LoginInProgressFactory, UserFactory
from meme_wars.tests import APITestCase
from meme_wars.utils import build_absolute_uri


@pytest.mark.django_db
class TestGoogleAuthCallbackQuerySerializer(APITestCase):
    faker = Faker()
    valid_data = {
        "state": uuid4().hex,
        "email": faker.email(),
        "given_name": faker.first_name(),
        "family_name": faker.last_name(),
        "picture": faker.image_url(),
    }

    def test_should_raise_validation_error_for_missing_session_data_for_login_in_progress(self):
        request = self.get_request_example(url_query_params={"a": "b"})
        serializer = GoogleAuthCallbackQuerySerializer(request=request)
        with self.raisesAPIValidationError(match="'login_in_progress'", code="login_in_progress_error"):
            serializer.is_valid(raise_exception=True)

    @patch.object(
        target=google_auth_callback_query_serializer,
        attribute=LoginInProgress.__name__,
        return_value=LoginInProgressFactory(),
    )
    def test_should_raise_validation_error_when_state_from_url_is_not_equal_to_state_from_session(self, _):
        request = self.get_request_example(url_query_params={"state": "xyz"})
        request.session["google_auth_state"] = "abc"
        serializer = GoogleAuthCallbackQuerySerializer(request=request)
        with self.raisesAPIValidationError(match="Access denied.", code="access_denied"):
            serializer.is_valid(raise_exception=True)

    @patch.object(GoogleAuthCallbackQuerySerializer, "_set_login_in_progress")
    @patch.object(GoogleAuthCallbackQuerySerializer, "_validate_google_auth_state")
    @patch.object(GoogleAuthCallbackQuerySerializer, "_get_user_id_token_data")
    def test_should_raise_validation_error_when_user_email_is_not_allowed(self, *_):
        request = self.get_request_example()
        serializer = GoogleAuthCallbackQuerySerializer(request=request)
        with self.raisesAPIValidationError(match="This email is not allowed.", code="forbidden_email"):
            serializer.is_valid(raise_exception=True)

    @patch.object(UserSettings, "validate_email")
    @patch.object(GoogleAuthCallbackQuerySerializer, "_get_user_id_token_data")
    def test_should_return_initial_data(self, mock_get_user_id_token_data, _):
        id_token_data = self.valid_data.copy()
        google_auth_state = id_token_data.pop("state")
        mock_get_user_id_token_data.return_value = id_token_data

        request = self.get_request_example(url_query_params={"state": google_auth_state})
        serializer = GoogleAuthCallbackQuerySerializer(request=request)

        initial_data = serializer._get_initial_data()
        self.assertEqual(initial_data, self.valid_data)

    @patch.object(
        target=GoogleAuthCallbackQuerySerializer, attribute="_create_token_endpoint_request_data", return_value={}
    )
    @patch.object(google_auth_callback_query_serializer.requests, "post")
    def test_should_return_user_id_token(self, mock_requests_post, _):
        class ResponseMock:
            id_token = "response-mock-id-token"

            def json(self) -> dict:
                return {"id_token": self.id_token}

        mock_requests_post.return_value = ResponseMock()
        request = self.get_request_example()
        serializer = GoogleAuthCallbackQuerySerializer(request=request)
        id_token = serializer._get_user_id_token()
        self.assertEqual(id_token, ResponseMock.id_token)

    @patch.object(GoogleAuthCallbackQuerySerializer, "_get_user_id_token", return_value="jwt-token")
    @patch.object(google_auth_callback_query_serializer.jwt, "decode")
    def test_should_return_user_id_token_data(self, mock_decode_jwt, _):
        mock_decode_jwt.return_value = {"key": "value"}

        request = self.get_request_example()
        serializer = GoogleAuthCallbackQuerySerializer(request=request)

        actual_user_id_token_data = serializer._get_user_id_token_data()
        self.assertEqual(actual_user_id_token_data, mock_decode_jwt.return_value)

    def test_should_create_token_endpoint_request_data(self):
        url_query_params = {
            "code": "xyz",
        }
        request = self.get_request_example(url_query_params=url_query_params)
        serializer = GoogleAuthCallbackQuerySerializer(request=request)
        request_data = serializer._create_token_endpoint_request_data()
        self.assertEqual(request_data["code"], url_query_params["code"])
        self.assertEqual(request_data["client_id"], settings.GOOGLE_OPENID_CLIENT_ID)
        self.assertEqual(request_data["client_secret"], settings.GOOGLE_OPENID_CLIENT_SECRET)
        expected_redirect_uri = build_absolute_uri(view_name="api:users:google_auth:callback")
        self.assertEqual(request_data["redirect_uri"], expected_redirect_uri)
        self.assertEqual(request_data["grant_type"], "authorization_code")

    @patch.object(google_auth_callback_query_serializer, "get_or_create_user")
    @patch.object(GoogleAuthCallbackQuerySerializer, "_get_google_user")
    def test_should_create_and_return_new_user(self, _, mock_get_or_create_user):
        mock_get_or_create_user.return_value = [UserFactory(), True]
        request = self.get_request_example()
        serializer = GoogleAuthCallbackQuerySerializer(request=request)
        user, is_created = serializer.get_or_create_user()
        self.assertTrue(is_created)
        self.assertEqual(user, mock_get_or_create_user.return_value[0])

    @patch.object(google_auth_callback_query_serializer, "get_or_create_user")
    @patch.object(GoogleAuthCallbackQuerySerializer, "_get_google_user")
    def test_should_return_existing_user(self, _, mock_get_or_create_user):
        mock_get_or_create_user.return_value = [UserFactory(), False]
        request = self.get_request_example()
        serializer = GoogleAuthCallbackQuerySerializer(request=request)
        user, is_created = serializer.get_or_create_user()
        self.assertFalse(is_created)
        self.assertEqual(user, mock_get_or_create_user.return_value[0])

    @patch.object(GoogleAuthCallbackQuerySerializer, "_set_login_in_progress")
    @patch.object(GoogleAuthCallbackQuerySerializer, "_validate_google_auth_state")
    @patch.object(GoogleAuthCallbackQuerySerializer, "_get_initial_data", return_value=valid_data)
    def test_should_return_google_user(self, *_):
        request = self.get_request_example(url_query_params={"state": "google-auth-state"})
        serializer = GoogleAuthCallbackQuerySerializer(request=request)
        serializer.is_valid(raise_exception=True)

        google_user = serializer._get_google_user()
        self.assertEqual(google_user.email, self.valid_data["email"])
        self.assertEqual(google_user.given_name, self.valid_data["given_name"])
        self.assertEqual(google_user.family_name, self.valid_data["family_name"])
        self.assertEqual(google_user.picture, self.valid_data["picture"])

    def test_should_raise_assertion_error_when_calling_build_login_failure_url_without_calling_is_valid_first(self):
        request = self.get_request_example()
        serializer = GoogleAuthCallbackQuerySerializer(request=request)

        expected_error_message = re.escape("You must call `.is_valid()` before accessing `.errors`.")
        with pytest.raises(expected_exception=AssertionError, match=expected_error_message):
            serializer.build_login_failure_url()

    @patch.object(
        target=google_auth_callback_query_serializer,
        attribute=LoginInProgress.__name__,
        return_value=LoginInProgressFactory(),
    )
    @patch.object(GoogleAuthCallbackQuerySerializer, "_validate_google_auth_state")
    @patch.object(GoogleAuthCallbackQuerySerializer, "_get_initial_data", return_value=valid_data)
    def test_should_raise_index_error_when_calling_build_login_failure_url_without_validation_errors(self, *_):
        request = self.get_request_example()
        serializer = GoogleAuthCallbackQuerySerializer(request=request)
        login_in_progress = LoginInProgressFactory()
        serializer._login_in_progress = login_in_progress

        self.assertTrue(serializer.is_valid())

        with pytest.raises(expected_exception=IndexError, match="list index out of range"):
            serializer.build_login_failure_url()

    def test_should_build_login_failure_url_when_validation_error_is_raised(self):
        request = self.get_request_example()
        serializer = GoogleAuthCallbackQuerySerializer(request=request)
        login_in_progress = LoginInProgressFactory()
        serializer._login_in_progress = login_in_progress

        # Should fail validation as soon as run_validation method in the serializer
        # is called, when setting LoginInProgress (because nothing is mocked)
        self.assertFalse(serializer.is_valid())

        url = serializer.build_login_failure_url()
        self.assertTrue(url.startswith(login_in_progress.login_failure_redirect_url))
        url_query_params = dict(parse.parse_qsl(parse.urlsplit(url).query))
        self.assertEqual(url_query_params["code"], "login_in_progress_error")

    def test_should_build_login_success_url_with_token_data(self):
        request = self.get_request_example()
        serializer = GoogleAuthCallbackQuerySerializer(request=request)
        login_in_progress = LoginInProgressFactory()
        serializer._login_in_progress = login_in_progress

        user = UserFactory(image_url=Faker().url())
        token = Token.objects.create(user=user)

        url = serializer.build_login_success_url(token=token)
        self.assertTrue(url.startswith(login_in_progress.login_success_redirect_url))
        url_query_params = dict(parse.parse_qsl(parse.urlsplit(url).query))
        self.assertEqual(url_query_params["token"], token.key)
        self.assertEqual(url_query_params["email"], token.user.email)
        self.assertEqual(url_query_params["first_name"], token.user.first_name)
        self.assertEqual(url_query_params["last_name"], token.user.last_name)
        self.assertEqual(url_query_params["image_url"], token.user.image_url)
