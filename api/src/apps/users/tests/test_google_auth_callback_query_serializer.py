from uuid import uuid4
from urllib import parse

from faker import Faker
import pytest
from unittest.mock import patch
from django.conf import settings
from rest_framework.authtoken.models import Token

from apps.common.tests import APITestCase
from apps.common.utils import build_absolute_uri
from apps.users.models import LoginInProgress
from apps.users.tests.factories import UserFactory, LoginInProgressFactory
from apps.users.serializers import (
    google_auth_callback_query_serializer,
    GoogleAuthCallbackQuerySerializer,
)


@pytest.mark.django_db
class TestGoogleAuthCallbackQuerySerializer(APITestCase):

    def test_should_raise_validation_error_for_missing_session_data_for_login_in_progress(self):
        request = self.get_request_example(url_query_params={'a': 'b'})
        serializer = GoogleAuthCallbackQuerySerializer(request=request)
        with self.raisesAPIValidationError(match="'login_in_progress'", code='login_in_progress_error'):
            serializer.is_valid(raise_exception=True)

    @patch.object(
        target=google_auth_callback_query_serializer,
        attribute=LoginInProgress.__name__,
        return_value=LoginInProgressFactory()
    )
    def test_should_raise_validation_error_when_state_from_url_is_not_equal_to_state_from_session(self, *_):
        request = self.get_request_example(url_query_params={'state': 'xyz'})
        request.session['google_auth_state'] = 'abc'
        serializer = GoogleAuthCallbackQuerySerializer(request=request)
        with self.raisesAPIValidationError(match='Access denied.', code='access_denied'):
            serializer.is_valid(raise_exception=True)

    @patch.object(GoogleAuthCallbackQuerySerializer, '_set_login_in_progress')
    @patch.object(GoogleAuthCallbackQuerySerializer, '_validate_google_auth_state')
    @patch.object(GoogleAuthCallbackQuerySerializer, '_get_user_id_token_data')
    def test_should_raise_validation_error_when_user_email_is_not_allowed(self, a, b, mock_decode):
        mock_decode.return_value = {'email', 'example@example.com'}

        request = self.get_request_example()
        serializer = GoogleAuthCallbackQuerySerializer(request=request)
        with self.raisesAPIValidationError(match='This email is not allowed.', code='forbidden_email'):
            serializer.is_valid(raise_exception=True)

    @patch.object(GoogleAuthCallbackQuerySerializer, '_set_login_in_progress')
    @patch.object(GoogleAuthCallbackQuerySerializer, '_validate_google_auth_state')
    @patch.object(GoogleAuthCallbackQuerySerializer, '_get_initial_data')
    def test_should_return_google_user(self, mock_get_initial_data, *_):
        faker = Faker()
        initial_data = {
            'state': uuid4().hex,
            'email': faker.email(),
            'given_name': faker.first_name(),
            'family_name': faker.last_name(),
            'picture': faker.image_url(),
        }
        mock_get_initial_data.return_value = initial_data

        request = self.get_request_example(url_query_params={'state': 'google-auth-state'})
        serializer = GoogleAuthCallbackQuerySerializer(request=request)
        serializer.is_valid(raise_exception=True)

        google_user = serializer._get_google_user()
        self.assertEqual(google_user.email, initial_data['email'])
        self.assertEqual(google_user.given_name, initial_data['given_name'])
        self.assertEqual(google_user.family_name, initial_data['family_name'])
        self.assertEqual(google_user.picture, initial_data['picture'])

    @patch.object(
        target=GoogleAuthCallbackQuerySerializer,
        attribute='_create_token_endpoint_request_data',
        return_value={}
    )
    @patch.object(google_auth_callback_query_serializer.requests, 'post')
    def test_should_get_user_id_token(self, mock_requests_post, _):
        class ResponseMock:
            id_token = 'response-mock-id-token'

            def json(self) -> dict:
                return {'id_token': self.id_token}

        mock_requests_post.return_value = ResponseMock()
        request = self.get_request_example()
        serializer = GoogleAuthCallbackQuerySerializer(request=request)
        id_token = serializer._get_user_id_token()
        self.assertEqual(id_token, ResponseMock.id_token)

    def test_should_return_token_endpoint_request_data(self):
        url_query_params = {
            'code': 'xyz',
        }
        request = self.get_request_example(url_query_params=url_query_params)
        serializer = GoogleAuthCallbackQuerySerializer(request=request)
        request_data = serializer._create_token_endpoint_request_data()
        self.assertEqual(request_data['code'], url_query_params['code'])
        self.assertEqual(request_data['client_id'], settings.GOOGLE_OPENID_CLIENT_ID)
        self.assertEqual(request_data['client_secret'], settings.GOOGLE_OPENID_CLIENT_SECRET)
        expected_redirect_uri = build_absolute_uri(view_name='api:users:google_auth:callback')
        self.assertEqual(request_data['redirect_uri'], expected_redirect_uri)
        self.assertEqual(request_data['grant_type'], 'authorization_code')

    @patch.object(google_auth_callback_query_serializer, 'get_or_create_user')
    @patch.object(GoogleAuthCallbackQuerySerializer, '_get_google_user')
    def test_should_create_user(self, _, mock_get_or_create_user):
        mock_get_or_create_user.return_value = [UserFactory(), True]
        request = self.get_request_example()
        serializer = GoogleAuthCallbackQuerySerializer(request=request)
        user, is_created = serializer.get_or_create_user()
        self.assertTrue(is_created)
        self.assertEqual(user, mock_get_or_create_user.return_value[0])

    @patch.object(google_auth_callback_query_serializer, 'get_or_create_user')
    @patch.object(GoogleAuthCallbackQuerySerializer, '_get_google_user')
    def test_should_get_user(self, _, mock_get_or_create_user):
        mock_get_or_create_user.return_value = [UserFactory(), False]
        request = self.get_request_example()
        serializer = GoogleAuthCallbackQuerySerializer(request=request)
        user, is_created = serializer.get_or_create_user()
        self.assertFalse(is_created)
        self.assertEqual(user, mock_get_or_create_user.return_value[0])

    def test_should_build_login_failure_url_when_validation_error_is_raised(self):
        # TODO
        pass

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
        self.assertEqual(url_query_params['token'], token.key)
        self.assertEqual(url_query_params['email'], token.user.email)
        self.assertEqual(url_query_params['first_name'], token.user.first_name)
        self.assertEqual(url_query_params['last_name'], token.user.last_name)
        self.assertEqual(url_query_params['image_url'], token.user.image_url)
